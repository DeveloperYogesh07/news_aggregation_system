from fastapi import FastAPI
from app.core.config import settings
from app.api.v1 import auth, users, articles, notifications, admin, saved_articles
from app.tasks.scheduler import start_scheduler
from app.core.database import engine, Base
from app.api.v1 import admin_creation

Base.metadata.create_all(bind=engine)

app = FastAPI(title="News Aggregator API")

# start_scheduler()


app.include_router(
    auth.router, prefix=settings.API_V1_STR + "/auth", tags=["Authentication"]
)
app.include_router(users.router, prefix=settings.API_V1_STR + "/users", tags=["Users"])

app.include_router(
    articles.router, prefix=settings.API_V1_STR + "/articles", tags=["Articles"]
)
app.include_router(
    notifications.router,
    prefix=settings.API_V1_STR + "/notifications",
    tags=["Notifications"],
)
app.include_router(admin.router, prefix=settings.API_V1_STR + "/admin", tags=["Admin"])

app.include_router(
    saved_articles.router,
    prefix=settings.API_V1_STR + "/saved-articles",
    tags=["Saved Articles"],
)

# app.include_router(admin_creation.router, prefix="/api/v1/utils", tags=["Utilities"])


@app.get("/")
def root():
    return {"message": "Welcome to News Aggregator API"}
