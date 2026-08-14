from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Farm
from app.schemas.schemas import FarmCreate, FarmUpdate, FarmOut, FieldCreate, FieldOut
from app.services.farm_service import create_farm, add_field
from app.utils.security import get_current_user, require_roles

router = APIRouter(tags=["Farms & Fields"])

@router.post("/farms", response_model=FarmOut, status_code=201)
def post_farm(data: FarmCreate, db: Session = Depends(get_db), _=Depends(require_roles("Admin","Farm Manager"))):
    return create_farm(db, data)

@router.get("/farms", response_model=list[FarmOut])
def get_farms(location: str|None=None, status: str|None=None, page: int=1, limit: int=10, sort_by: str="id", sort_order: str="asc", db: Session=Depends(get_db), _=Depends(get_current_user)):
    q = db.query(Farm)
    if location: q = q.filter(Farm.location.ilike(f"%{location}%"))
    if status: q = q.filter(Farm.status == status)
    column = getattr(Farm, sort_by, Farm.id)
    q = q.order_by(column.desc() if sort_order.lower()=="desc" else column.asc())
    return q.offset((max(page,1)-1)*limit).limit(min(max(limit,1),100)).all()

@router.get("/farms/{farm_id}", response_model=FarmOut)
def get_farm(farm_id:int, db:Session=Depends(get_db), _=Depends(get_current_user)):
    obj=db.get(Farm,farm_id)
    if not obj: raise HTTPException(404,"Farm not found")
    return obj

@router.put("/farms/{farm_id}", response_model=FarmOut)
def update_farm(farm_id:int, data:FarmUpdate, db:Session=Depends(get_db), _=Depends(require_roles("Admin","Farm Manager"))):
    obj=db.get(Farm,farm_id)
    if not obj: raise HTTPException(404,"Farm not found")
    values=data.model_dump(exclude_unset=True)
    if "farm_name" in values and db.query(Farm).filter(Farm.farm_name==values["farm_name"], Farm.id!=farm_id).first():
        raise HTTPException(409,"Farm name already exists")
    if "total_area" in values and values["total_area"] < sum(f.area for f in obj.fields):
        raise HTTPException(400,"Total farm area cannot be less than already allocated field area")
    for k,v in values.items(): setattr(obj,k,v)
    db.commit(); db.refresh(obj); return obj

@router.post("/farms/{farm_id}/fields", response_model=FieldOut, status_code=201)
def post_field(farm_id:int,data:FieldCreate,db:Session=Depends(get_db),_=Depends(require_roles("Admin","Farm Manager","Farmer"))):
    return add_field(db,farm_id,data)

@router.get("/farms/{farm_id}/fields", response_model=list[FieldOut])
def get_fields(farm_id:int,db:Session=Depends(get_db),_=Depends(get_current_user)):
    farm=db.get(Farm,farm_id)
    if not farm: raise HTTPException(404,"Farm not found")
    return farm.fields
