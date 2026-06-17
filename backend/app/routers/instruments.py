from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.models.models import Instrument
from app.schemas.schemas import InstrumentOut, InstrumentCreate
from app.routers.auth import get_current_user, require_role

router = APIRouter()

@router.get("", response_model=List[InstrumentOut])
def list_instruments(status: Optional[str] = None, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    q = db.query(Instrument)
    if status: q = q.filter(Instrument.status == status)
    return q.order_by(Instrument.created_at.desc()).all()

@router.post("", response_model=InstrumentOut)
def create_instrument(data: InstrumentCreate, db: Session = Depends(get_db), _=require_role("admin", "manager")):
    i = Instrument(**data.dict()); db.add(i); db.commit(); db.refresh(i); return i

@router.put("/{iid}", response_model=InstrumentOut)
def update_instrument(iid: int, data: InstrumentCreate, db: Session = Depends(get_db), _=require_role("admin", "manager")):
    i = db.query(Instrument).filter(Instrument.id == iid).first()
    if not i: raise HTTPException(status_code=404, detail="乐器不存在")
    for k, v in data.dict().items(): setattr(i, k, v)
    db.commit(); db.refresh(i); return i

@router.post("/{iid}/status")
def update_status(iid: int, status: str, db: Session = Depends(get_db), _=require_role("admin", "manager", "teacher")):
    i = db.query(Instrument).filter(Instrument.id == iid).first()
    if not i: raise HTTPException(status_code=404, detail="乐器不存在")
    i.status = status; db.commit()
    return {"message": "状态已更新"}

@router.delete("/{iid}")
def delete_instrument(iid: int, db: Session = Depends(get_db), _=require_role("admin")):
    i = db.query(Instrument).filter(Instrument.id == iid).first()
    if not i: raise HTTPException(status_code=404, detail="乐器不存在")
    db.delete(i); db.commit()
    return {"message": "乐器已删除"}
