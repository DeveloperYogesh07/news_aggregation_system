from apscheduler.schedulers.background import BackgroundScheduler
from app.core.database import SessionLocal
from app.services.news_service import NewsService


def fetch_external_news_periodically():
    db = SessionLocal()
    try:
        service = NewsService(db)
        service.fetch_and_store_top_headlines()
    finally:
        db.close()


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(fetch_external_news_periodically, "interval", minutes=30)
    scheduler.start()
