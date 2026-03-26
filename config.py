"""
config.py — Loyiha konfiguratsiyasi
Barcha sozlamalar shu yerda, .env fayldan o'qiladi
"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# === PATHS ===
BASE_DIR      = Path(__file__).parent
DATA_DIR      = BASE_DIR / "data"
RAW_DIR       = DATA_DIR / "raw"
CLEANED_DIR   = DATA_DIR / "cleaned"
FINAL_DIR     = DATA_DIR / "final"

for d in [RAW_DIR, CLEANED_DIR, FINAL_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# === TELEGRAM ===
TELEGRAM_API_ID   = os.getenv("TELEGRAM_API_ID", "")
TELEGRAM_API_HASH = os.getenv("TELEGRAM_API_HASH", "")
TELEGRAM_PHONE    = os.getenv("TELEGRAM_PHONE", "")

# O'zbekistondagi biznes dasturlar haqida Telegram kanallar
TELEGRAM_CHANNELS = [
    "uzcrm",
    "uzbek_erp",
    "1c_uzbekistan",
    "itpark_uz",
    "techuz",
    "startupuz",
]

# === SCRAPING SETTINGS ===
REQUEST_DELAY_MIN = 2   # sekund
REQUEST_DELAY_MAX = 5   # sekund
MAX_RETRIES       = 3
TIMEOUT           = 30  # sekund

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "uz-UZ,uz;q=0.9,en-US;q=0.8,en;q=0.7,ru;q=0.6",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

# === KATEGORIYALAR ===
CATEGORIES = {
    "CRM":          ["crm", "mijozlar", "sales", "savdo", "customer"],
    "ERP":          ["erp", "enterprise", "1c", "1s", "buxgalteriya", "accounting"],
    "HR":           ["hr", "kadrlar", "xodimlar", "payroll", "maosh", "human resource"],
    "POS":          ["pos", "kassa", "retail", "savdo nuqtasi", "point of sale"],
    "Loyiha":       ["project", "loyiha", "task", "trello", "jira", "asana"],
    "Moliya":       ["finance", "moliya", "bank", "to'lov", "payment", "invoice"],
    "Omborxona":    ["warehouse", "ombor", "inventory", "zaxira", "stock"],
    "Marketing":    ["marketing", "reklama", "sms", "email marketing", "campaign"],
}

# === G2 / CAPTERRA SEARCH QUERIES ===
G2_SEARCH_QUERIES = [
    "crm software uzbekistan",
    "erp software central asia",
    "hr software uzbekistan",
    "pos software uzbekistan",
    "accounting software uzbekistan",
]

CAPTERRA_CATEGORIES = [
    "crm-software",
    "erp-software",
    "hr-software",
    "pos-software",
    "accounting-software",
]

# === GOOGLE PLAY ===
PLAY_SEARCH_QUERIES = [
    "CRM O'zbekiston",
    "buxgalteriya dasturi",
    "kassa dasturi",
    "savdo dasturi uzbekistan",
    "HR management uzbekistan",
    "ERP uzbekistan",
]
PLAY_LANG   = "uz"
PLAY_COUNTRY = "uz"

# === OUTPUT ===
FINAL_CSV  = FINAL_DIR / "uzbekistan_biznes_dasturlari.csv"
FINAL_XLSX = FINAL_DIR / "uzbekistan_biznes_dasturlari.xlsx"