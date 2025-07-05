from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.external_source_service import ExternalSourceService
from app.schemas.external_source import ExternalSourceCreate, ExternalSourceRead, ExternalSourceUpdate
from app.schemas.category import CategoryCreate, CategoryRead
from app.services.category_service import CategoryService

router = APIRouter()

@router.post("/external-sources/", response_model=ExternalSourceRead)
def create_external_source(data: ExternalSourceCreate, db: Session = Depends(get_db)):
    service = ExternalSourceService(db)
    return service.create(data)

@router.get("/external-sources/", response_model=list[ExternalSourceRead])
def list_external_sources(db: Session = Depends(get_db)):
    service = ExternalSourceService(db)
    return service.list_sources()

@router.delete("/external-sources/{source_id}")
def delete_external_source(source_id: int, db: Session = Depends(get_db)):
    service = ExternalSourceService(db)
    source = service.delete(source_id)
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    return {"message": "Deleted"}

@router.put("/external-sources/{source_id}", response_model=ExternalSourceRead)
def update_external_source(source_id: int, data: ExternalSourceUpdate, db: Session = Depends(get_db)):
    service = ExternalSourceService(db)
    updated = service.update(source_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Source not found")
    return updated

@router.post("/categories/", response_model=CategoryRead)
def add_category(data: CategoryCreate, db: Session = Depends(get_db)):
    service = CategoryService(db)
    return service.create(data)

@router.get("/categories/", response_model=List[CategoryRead])
def list_categories(db: Session = Depends(get_db)):
    service = CategoryService(db)
    return service.get_all()