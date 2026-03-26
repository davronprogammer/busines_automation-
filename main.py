"""
main.py — Asosiy pipeline orkestratori
Barcha bosqichlarni ketma-ket ishga tushiradi.

ISHLATISH:
  python main.py             # To'liq pipeline (scraping + cleaning + transform + dataset)
  python main.py --sample    # Faqat sample data (scraping yo'q, tezkor test)
  python main.py --clean     # Faqat cleaning + transformation (raw data mavjud bo'lsa)
  python main.py --dashboard # Faqat dashboard (data mavjud bo'lsa)
"""
import sys
import asyncio
import argparse
from loguru import logger
from pathlib import Path


# ─── Logger sozlamasi ─────────────────────────────────────────────────────────
logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | {message}",
    colorize=True,
)
logger.add(
    "data/pipeline.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    rotation="10 MB",
)


def parse_args():
    parser = argparse.ArgumentParser(
        description="O'zbekiston biznes dasturlari tahlil pipeline"
    )
    parser.add_argument("--sample",    action="store_true", help="Sample data bilan ishlash")
    parser.add_argument("--clean",     action="store_true", help="Faqat cleaning bosqichi")
    parser.add_argument("--dashboard", action="store_true", help="Dashboardni ishga tushirish")
    parser.add_argument("--no-telegram", action="store_true", help="Telegram scraping o'tkazib yuborish")
    parser.add_argument("--no-gplay",    action="store_true", help="Google Play scraping o'tkazib yuborish")
    return parser.parse_args()


async def run_scrapers(skip_telegram: bool = False, skip_gplay: bool = False):
    """Barcha scraperlarni parallel/ketma-ket ishga tushiradi."""
    logger.info("╔══════════════════════════════════╗")
    logger.info("║   SCRAPING BOSQICHI BOSHLANDI    ║")
    logger.info("╚══════════════════════════════════╝")

    all_results = []

    # 1. G2 + Capterra (Playwright, async)
    try:
        from scrapers.g2_capterra_scraper import run_g2_capterra
        results = await run_g2_capterra()
        all_results.extend(results)
        logger.success(f"✓ G2 + Capterra: {len(results)} yozuv")
    except Exception as e:
        logger.error(f"G2/Capterra xato: {e}")

    # 2. OLX + Torg.uz
    try:
        from scrapers.local_scraper import run_local_scrapers
        results = run_local_scrapers()
        all_results.extend(results)
        logger.success(f"✓ OLX + Torg.uz: {len(results)} yozuv")
    except Exception as e:
        logger.error(f"Mahalliy saytlar xato: {e}")

    # 3. Telegram (ixtiyoriy)
    if not skip_telegram:
        try:
            from scrapers.telegram_scraper import run_telegram_scraper
            results = await run_telegram_scraper(days_back=30)
            all_results.extend(results)
            logger.success(f"✓ Telegram: {len(results)} yozuv")
        except Exception as e:
            logger.warning(f"Telegram o'tkazib yuborildi: {e}")

    # 4. Google Play (ixtiyoriy)
    if not skip_gplay:
        try:
            from scrapers.google_play_scraper import run_google_play_scraper
            results = run_google_play_scraper()
            all_results.extend(results)
            logger.success(f"✓ Google Play: {len(results)} yozuv")
        except Exception as e:
            logger.warning(f"Google Play o'tkazib yuborildi: {e}")

    logger.success(f"Scraping yakunlandi: jami {len(all_results)} yozuv")
    return all_results


def run_pipeline(df=None):
    """Cleaning → Transformation → Dataset"""
    logger.info("╔══════════════════════════════════╗")
    logger.info("║     PIPELINE BOSHLANDI           ║")
    logger.info("╚══════════════════════════════════╝")

    from pipeline.cleaner      import run_cleaning
    from pipeline.transformer  import run_transformation
    from pipeline.dataset_builder import build_final_dataset

    if df is None:
        df = run_cleaning()
    df = run_transformation(df)
    df = build_final_dataset(df)
    return df


def launch_dashboard():
    """Streamlit dashboardni ishga tushiradi."""
    import subprocess
    logger.info("Dashboard ishga tushirilmoqda: http://localhost:8501")
    subprocess.run([
        sys.executable, "-m", "streamlit", "run",
        "dashboard/app.py",
        "--server.port", "8501",
        "--server.address", "localhost",
        "--theme.base", "dark",
    ])


def main():
    args = parse_args()

    logger.info("=" * 50)
    logger.info("O'ZBEKISTON BIZNES DASTURLARI PIPELINE")
    logger.info("=" * 50)

    if args.dashboard:
        launch_dashboard()
        return

    if args.sample:
        # Scraping o'tkazib yuborib sample data ishlatamiz
        logger.info("SAMPLE MODE: Real scraping yo'q")
        from pipeline.dataset_builder import generate_sample_dataset
        df = generate_sample_dataset()
        df = run_pipeline(df)

    elif args.clean:
        # Faqat cleaning (raw data mavjud bo'lishi kerak)
        df = run_pipeline()

    else:
        # To'liq pipeline
        df = asyncio.run(run_scrapers(
            skip_telegram=args.no_telegram,
            skip_gplay=args.no_gplay,
        ))
        df = run_pipeline()

    logger.success("Pipeline muvaffaqiyatli yakunlandi! ✅")
    logger.info("Dashboard ishga tushirish uchun: streamlit run dashboard/app.py")
    return df


if __name__ == "__main__":
    main()