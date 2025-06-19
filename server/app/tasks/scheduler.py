from apscheduler.schedulers.background import BackgroundScheduler
from app.core.database import SessionLocal
from app.services.news_service import NewsService


def fetch_external_news_periodically():
    db = SessionLocal()
    try:
        print("Fetching external news...")
        service = NewsService(db)
        service.fetch_and_store_top_headlines()
        print("News fetched successfully")
    finally:
        db.close()


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        fetch_external_news_periodically, "interval", hours=4
    )  
    scheduler.start()
