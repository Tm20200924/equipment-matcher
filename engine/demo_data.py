# -*- coding: utf-8 -*-
"""Demo product database for Streamlit Cloud deployment.
Replace with real data via Google Drive in production."""

DEMO_PRODUCTS = [
    {"model": "920E", "category": "EX", "desc_ru": "Гусеничный экскаватор 920E", "desc_cn": "履带式挖掘机920E",
     "tonnage": 20.0, "hp": 150, "bucket_m3": 0.9, "dap_price_cny": 464000, "scrap_tax_rub": 600000, "engine": "Cummins"},
    {"model": "922E", "category": "EX", "desc_ru": "Гусеничный экскаватор 922E", "desc_cn": "履带式挖掘机922E",
     "tonnage": 22.0, "hp": 170, "bucket_m3": 1.0, "dap_price_cny": 484000, "scrap_tax_rub": 650000, "engine": "Cummins"},
    {"model": "936E", "category": "EX", "desc_ru": "Гусеничный экскаватор 936E", "desc_cn": "履带式挖掘机936E",
     "tonnage": 36.0, "hp": 280, "bucket_m3": 1.6, "dap_price_cny": 820000, "scrap_tax_rub": 1000000, "engine": "Cummins"},
    {"model": "950E", "category": "EX", "desc_ru": "Гусеничный экскаватор 950E", "desc_cn": "履带式挖掘机950E",
     "tonnage": 50.0, "hp": 370, "bucket_m3": 2.5, "dap_price_cny": 1200000, "scrap_tax_rub": 1500000, "engine": "Cummins"},
    {"model": "9018F", "category": "EX", "desc_ru": "Мини-экскаватор 9018F", "desc_cn": "微型挖掘机9018F",
     "tonnage": 1.8, "hp": 18, "bucket_m3": 0.04, "dap_price_cny": 100000, "scrap_tax_rub": 100000, "engine": "Yanmar"},
    {"model": "835H", "category": "WL", "desc_ru": "Фронтальный погрузчик 835H", "desc_cn": "装载机835H",
     "tonnage": 10.9, "hp": 123, "bucket_m3": 1.8, "dap_price_cny": 192000, "scrap_tax_rub": 300000, "engine": "Yuchai"},
    {"model": "856H", "category": "WL", "desc_ru": "Фронтальный погрузчик 856H", "desc_cn": "装载机856H",
     "tonnage": 5.6, "hp": 160, "bucket_m3": 3.0, "dap_price_cny": 350000, "scrap_tax_rub": 400000, "engine": "Weichai"},
    {"model": "848T", "category": "WL", "desc_ru": "Фронтальный погрузчик 848T", "desc_cn": "装载机848T",
     "tonnage": 4.8, "hp": 220, "bucket_m3": 2.5, "dap_price_cny": 420000, "scrap_tax_rub": 450000, "engine": "Weichai"},
    {"model": "B260", "category": "BD", "desc_ru": "Бульдозер B260", "desc_cn": "推土机B260",
     "tonnage": 26.0, "hp": 260, "bucket_m3": 0, "dap_price_cny": 728000, "scrap_tax_rub": 700000, "engine": "Weichai"},
    {"model": "B160C", "category": "BD", "desc_ru": "Бульдозер B160C", "desc_cn": "推土机B160C",
     "tonnage": 16.0, "hp": 160, "bucket_m3": 0, "dap_price_cny": 388000, "scrap_tax_rub": 400000, "engine": "Weichai"},
    {"model": "6032E", "category": "RL", "desc_ru": "Виброкаток 6032E", "desc_cn": "双钢轮压路机6032E",
     "tonnage": 3.2, "hp": 35, "bucket_m3": 0, "dap_price_cny": 153192, "scrap_tax_rub": 150000, "engine": "Kubota"},
    {"model": "6126E", "category": "RL", "desc_ru": "Виброкаток 6126E", "desc_cn": "单钢轮压路机6126E",
     "tonnage": 26.0, "hp": 160, "bucket_m3": 0, "dap_price_cny": 462800, "scrap_tax_rub": 450000, "engine": "Weichai"},
    {"model": "4140D", "category": "MG", "desc_ru": "Автогрейдер 4140D", "desc_cn": "平地机4140D",
     "tonnage": 14.0, "hp": 140, "bucket_m3": 0, "dap_price_cny": 438000, "scrap_tax_rub": 400000, "engine": "Weichai"},
    {"model": "DW90A", "category": "MT", "desc_ru": "Карьерный самосвал DW90A", "desc_cn": "矿用自卸车DW90A",
     "tonnage": 90.0, "hp": 480, "bucket_m3": 0, "dap_price_cny": 2500000, "scrap_tax_rub": 3000000, "engine": "Yuchai"},
    {"model": "777A", "category": "BHL", "desc_ru": "Экскаватор-погрузчик 777A", "desc_cn": "两头忙777A",
     "tonnage": 8.0, "hp": 97, "bucket_m3": 0.3, "dap_price_cny": 430000, "scrap_tax_rub": 400000, "engine": "Perkins"},
]

DEMO_COMPETITORS = {
    "XE370CA": ["XCMG", 37.0, 1.8],
    "XE215C": ["XCMG", 21.5, 0.9],
    "SY215C": ["SANY", 21.5, 0.9],
    "SY365H": ["SANY", 36.5, 1.8],
    "CAT320": ["CAT", 20.0, 0.9],
    "CAT336": ["CAT", 36.0, 1.8],
    "PC200-8": ["Komatsu", 20.0, 0.9],
    "PC360-7": ["Komatsu", 36.0, 1.8],
    "SD16": ["SHANTUI", 16.0, 0],
    "SD22": ["SHANTUI", 22.0, 0],
    "TY230": ["XCMG", 23.0, 0],
    "SD26": ["SHANTUI", 26.0, 0],
    "XS223H": ["XCMG", 22.0, 0],
}

def to_product_db():
    """Convert demo data to the format engine expects."""
    return {
        "meta": {"version": "demo", "total": len(DEMO_PRODUCTS)},
        "products": DEMO_PRODUCTS
    }

def to_competitor_db():
    """Convert demo data to competitor DB format."""
    return {
        "known": DEMO_COMPETITORS
    }
