# -*- coding: utf-8 -*-
import streamlit as st
st.set_page_config(page_title="设备智能匹配引擎 v19", page_icon="🔧", layout="wide")

import os, sys, json, io, traceback, re
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "engine"))
sys.path.insert(0, os.path.dirname(__file__))

errors = []
try: import pandas as pd
except Exception as e: pd = None; errors.append(f"pandas: {e}")

HAS_OPENPYXL = False
try: import openpyxl; HAS_OPENPYXL = True
except: pass

eng = None
try: import engine_v19 as eng
except Exception as e: errors.append(f"engine_v19: {e}")

@st.cache_resource
def init_data():
    config = {}; db = []
    if eng:
        try:
            eng.CONFIG_PATH = os.path.join(os.path.dirname(__file__), "engine", "config.json")
            eng.DB_PATH = os.path.join(os.path.dirname(__file__), "engine", "product_db_full.json")
            eng.COMP_DB_PATH = os.path.join(os.path.dirname(__file__), "engine", "competitor_db.json")
            config = eng.load_config(); db = eng.load_db()
        except Exception as e: errors.append(f"加载数据失败: {e}")
        if not db:
            try:
                from engine.demo_data import to_product_db, to_competitor_db
                with open(eng.DB_PATH, "w", encoding="utf-8") as f: json.dump(to_product_db(), f, ensure_ascii=False)
                with open(eng.COMP_DB_PATH, "w", encoding="utf-8") as f: json.dump(to_competitor_db(), f, ensure_ascii=False)
                db = eng.load_db()
            except Exception as e: errors.append(f"演示数据加载失败: {e}")
    if "config" in st.secrets:
        for k, v in st.secrets["config"].items(): config[k] = v
    return config, db, errors

config, db, init_errors = init_data()

# ========== 侧边栏 ==========
with st.sidebar:
    st.header("⚙️ 参数设置")
    if init_errors:
        with st.expander("⚠️ 警告"):
            for e in init_errors: st.warning(e)
    if not eng or not db:
        st.error("引擎未加载，请检查警告信息")
        st.stop()

    rate = st.number_input("汇率 (人民币→卢布)", value=float(config.get("exchange_rate_rub_cny", 11.5)), step=0.1)
    duty = st.number_input("关税 (%)", value=float(config.get("customs_duty_rate_pct", 5.0)), step=0.1)
    proc = st.number_input("报关手续费 (%)", value=float(config.get("customs_processing_rate_pct", 0.3)), step=0.1)
    vat = st.number_input("增值税 (%)", value=float(config.get("vat_rate_pct", 22.0)), step=0.1)
    warehouse = st.number_input("仓储费 (卢布)", value=int(config.get("customs_warehouse_fee_rub", 20000)), step=1000)
    customs_fee = st.number_input("海关费 (卢布)", value=int(config.get("customs_fee_rub", 6000)), step=1000)
    agent_fee = st.number_input("代理费 (卢布)", value=int(config.get("customs_agent_fee_rub", 30000)), step=1000)
    st.divider()
    st.caption(f"产品库: {len(db)} 个型号 | 引擎 v19")

config.update({
    "exchange_rate_rub_cny": rate, "customs_duty_rate_pct": duty,
    "customs_processing_rate_pct": proc, "vat_rate_pct": vat,
    "customs_warehouse_fee_rub": warehouse, "customs_fee_rub": customs_fee,
    "customs_agent_fee_rub": agent_fee
})

# ========== 主页 ==========
st.title("🔧 设备智能匹配引擎 v19")
st.caption("上传客户询盘 → 自动匹配产品型号 → 计算DAP满洲里到岸价(卢布) → 交叉验证")

tab1, tab2, tab3 = st.tabs(["📥 询盘输入", "📊 匹配结果", "✅ 验证报告"])

# ========== TAB 1: 输入 ==========
with tab1:
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("📎 上传询盘文件")
        uploaded = st.file_uploader("支持 Excel / CSV 格式", type=["xlsx", "xls", "csv"])
    with c2:
        st.subheader("✏️ 或手动粘贴")
        txt = st.text_area("每行一条询盘", height=150,
            placeholder="挖掘机 20吨 x2\n小型压路机 2-3t x6\n推土机 TY230 x4")

    if st.button("🚀 开始匹配", type="primary", use_container_width=True):
        inquiries = []
        if uploaded:
            ext = uploaded.name.rsplit(".", 1)[-1].lower()
            if ext in ("xlsx", "xls"):
                if HAS_OPENPYXL:
                    inquiries = eng.parse_inquiry_excel(uploaded)
                else:
                    st.warning("Excel解析需要openpyxl库，请使用CSV或粘贴文本")
            elif ext == "csv":
                if pd is not None:
                    df = pd.read_csv(io.BytesIO(uploaded.getvalue()))
                    for i, row in df.iterrows():
                        name = str(row.iloc[0])
                        qty = int(str(row.iloc[1])) if len(row) > 1 and str(row.iloc[1]).isdigit() else 1
                        inquiries.append({"seq": str(i+1), "name": name, "qty": qty})
            if inquiries:
                st.success(f"📋 从文件解析了 {len(inquiries)} 条询盘")

        if txt.strip():
            for i, line in enumerate(txt.strip().split("\n")):
                line = line.strip()
                if not line: continue
                qty = 1
                qm = re.search(r"x\s*(\d+)", line, re.IGNORECASE)
                if qm: qty = int(qm.group(1))
                inquiries.append({"seq": str(i+1), "name": line, "qty": qty})
            st.success(f"📋 从文本解析了 {len(inquiries)} 条询盘")

        if inquiries:
            st.session_state["inquiries"] = inquiries
            st.session_state["results"] = []
            with st.spinner("正在匹配产品..."):
                for item in inquiries:
                    cands, ton, bucket, ver = eng.match_products(item["name"], db, config)
                    st.session_state["results"].append({
                        "item": item, "candidates": cands,
                        "ton": ton, "bucket": bucket, "verification": ver
                    })
        elif not uploaded:
            st.warning("请上传文件或粘贴询盘内容")

# ========== TAB 2: 结果 ==========
with tab2:
    if "results" not in st.session_state:
        st.info("👈 请先在「询盘输入」完成匹配")
    else:
        results = st.session_state["results"]
        matched = sum(1 for r in results if r["candidates"])
        st.metric("匹配率", f"{matched} / {len(results)}")

        rows = []
        for r in results:
            item = r["item"]; cands = r["candidates"]
            cat = eng.classify_inquiry(item["name"]) or ""
            comp, _ = eng.detect_competitor(item["name"])
            if comp: cat = f"竞品({comp})" if not cat else f"{cat} / 竞品({comp})"

            if not cands:
                reason = "非自有产品" if eng.is_non_own(item["name"]) else "未找到匹配"
                rows.append({"序号": item["seq"], "客户询盘": item["name"], "数量": item["qty"],
                    "设备类别": cat or "N/A", "推荐型号": "--", "匹配度": "--",
                    "DAP到岸总价(卢布)": "--", "推荐理由": reason, "验证": "--"})
            else:
                for ci, cand in enumerate(cands[:2]):
                    p = cand["product"]
                    cost = eng.calc_dap(p.get("dap_price_cny", 0) or 0, p.get("scrap_tax_rub", 0) or 0, config)
                    reasons = "; ".join(cand["reasons"]) if cand["reasons"] else "--"
                    vl = (r.get("verification") or {}).get("top_verification") or {}
                    tag = "⭐ 推荐" if ci == 0 else f"备选{ci}"
                    rows.append({
                        "序号": item["seq"] if ci==0 else "",
                        "客户询盘": item["name"] if ci==0 else "",
                        "数量": item["qty"] if ci==0 else "",
                        "设备类别": cat if ci==0 else "",
                        "推荐型号": p["model"],
                        "匹配度": f'{cand["score"]}分 {tag}',
                        "DAP到岸总价(卢布)": f'{cost["total_rub"]:,.0f}',
                        "推荐理由": reasons,
                        "验证": vl.get("level", "")
                    })

        df = pd.DataFrame(rows) if pd is not None else None
        if df is not None:
            st.dataframe(df, use_container_width=True, height=500)
            csv = df.to_csv(index=False).encode("utf-8-sig")
            st.download_button("📥 下载CSV报告", csv, f"Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
        else:
            st.table(rows)

# ========== TAB 3: 验证 ==========
with tab3:
    if "results" not in st.session_state:
        st.info("👈 请先完成匹配")
    else:
        vr = []
        for r in st.session_state["results"]:
            v = (r.get("verification") or {})
            tv = v.get("top_verification") or {}
            vr.append({
                "询盘": r["item"]["name"][:40],
                "分类": v.get("classified_cat",""),
                "需求吨位": v.get("extracted_ton",0),
                "本地吨位": tv.get("local_ton",0),
                "联网吨位": tv.get("online_ton",0),
                "验证等级": tv.get("level",""),
            })
        if vr:
            st.subheader("🔍 交叉验证详情")
            labels = {"dual": "双重验证", "single": "单方验证", "conflict": "数据冲突", "close": "数据接近", "none": "无数据"}
            for i, v in enumerate(vr):
                v["验证等级"] = labels.get(v["验证等级"], v["验证等级"])
            st.dataframe(pd.DataFrame(vr) if pd else vr, use_container_width=True)
            c1,c2,c3 = st.columns(3)
            c1.metric("双重验证", sum(1 for v in vr if "双重" in str(v.get("验证等级",""))))
            c2.metric("单方验证", sum(1 for v in vr if "单方" in str(v.get("验证等级",""))))
            c3.metric("数据冲突", sum(1 for v in vr if "冲突" in str(v.get("验证等级",""))))

st.divider()
st.caption("设备智能匹配引擎 v19 | DAP满洲里到岸价 | github.com/Tm20200924/equipment-matcher")
