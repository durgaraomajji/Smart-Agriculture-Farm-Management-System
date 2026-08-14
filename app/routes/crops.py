from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Crop
from app.schemas.schemas import CropCreate,CropUpdate,CropOut
from app.services.crop_service import create_crop,update_crop
from app.utils.security import get_current_user,require_roles

router=APIRouter(tags=["Crops"])

@router.post("/crops",response_model=CropOut,status_code=201)
def post_crop(data:CropCreate,db:Session=Depends(get_db),_=Depends(require_roles("Admin","Farm Manager","Farmer"))):
    return create_crop(db,data)

@router.get("/crops",response_model=list[CropOut])
def get_crops(crop_name:str|None=None,status:str|None=None,start_date:date|None=None,end_date:date|None=None,page:int=1,limit:int=10,sort_by:str="id",sort_order:str="asc",db:Session=Depends(get_db),_=Depends(get_current_user)):
    q=db.query(Crop)
    if crop_name:q=q.filter(Crop.crop_name.ilike(f"%{crop_name}%"))
    if status:q=q.filter(Crop.status==status)
    if start_date:q=q.filter(Crop.planting_date>=start_date)
    if end_date:q=q.filter(Crop.planting_date<=end_date)
    col=getattr(Crop,sort_by,Crop.id)
    q=q.order_by(col.desc() if sort_order.lower()=="desc" else col.asc())
    return q.offset((max(page,1)-1)*limit).limit(min(max(limit,1),100)).all()

@router.get("/crops/{crop_id}",response_model=CropOut)
def get_crop(crop_id:int,db:Session=Depends(get_db),_=Depends(get_current_user)):
    obj=db.get(Crop,crop_id)
    if not obj:raise HTTPException(404,"Crop not found")
    return obj

@router.put("/crops/{crop_id}",response_model=CropOut)
def put_crop(crop_id:int,data:CropUpdate,db:Session=Depends(get_db),_=Depends(require_roles("Admin","Farm Manager","Farmer"))):
    obj=db.get(Crop,crop_id)
    if not obj:raise HTTPException(404,"Crop not found")
    return update_crop(db,obj,data)
