biznes_auto/
├── main.py                    ← Asosiy orkestratorar
├── config.py                  ← Barcha sozlamalar
├── requirements.txt           ← Kutubxonalar
├── .env                       ← Maxfiy kalitlar (git ignore!)
│
├── scrapers/
│   ├── g2_capterra_scraper.py ← G2 va Capterra (Playwright)
│   ├── local_scraper.py       ← OLX.uz va Torg.uz (BeautifulSoup)
│   ├── telegram_scraper.py    ← Telegram kanallar (Telethon)
│   └── google_play_scraper.py ← Google Play Store
│
├── pipeline/
│   ├── cleaner.py             ← Ma'lumotlarni tozalash
│   ├── transformer.py         ← Transformatsiya va boyitish
│   └── dataset_builder.py     ← Final dataset + sample data
│
├── data/
│   ├── raw/                   ← Scraperlardan tushgan xom data
│   ├── cleaned/               ← Tozalangan data
│   └── final/                 ← Tayyor dataset (CSV + XLSX)
│
├── dashboard/
│   └── app.py                 ← Streamlit dashboard (6 tab)
│
└── utils/
    └── helpers.py             ← Umumiy yordamchi funksiyalar