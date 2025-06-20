from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_password_hash
from app.models.user import User

router = APIRouter()

@router.post("/create-admin")
def create_admin(db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == "admin@gmail.com").first()
    if existing:
        return {"message": "Admin user already exists."}

    hashed_password = get_password_hash("123")
    admin_user = User(
        username="admin",
        email="admin@gmail.com",
        hashed_password=hashed_password,
        is_admin=True,
        is_active=True
    )
    db.add(admin_user)
    db.commit()
    return {"message": "Admin user created successfully"}
