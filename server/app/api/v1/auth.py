from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.auth_service import AuthService
from app.schemas.auth import Token, LoginRequest
from app.schemas.user import UserCreate

router = APIRouter()

@router.post("/signup", response_model=Token)
def signup(user_create: UserCreate, db: Session = Depends(get_db)):
    service = AuthService(db)
    try:
        return service.register_user(user_create)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/login", response_model=Token)
def login(login_req: LoginRequest, db: Session = Depends(get_db)):
    service = AuthService(db)
    try:
        return service.authenticate_user(login_req.email, login_req.password)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
