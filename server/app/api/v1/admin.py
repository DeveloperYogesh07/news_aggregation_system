from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.external_source_service import ExternalSourceService
from app.schemas.external_source import ExternalSourceCreate, ExternalSourceRead

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
