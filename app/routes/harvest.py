from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Crop,Harvest
from app.schemas.schemas import HarvestCreate,HarvestOut
from app.utils.security import get_current_user,require_roles

router=APIRouter(tags=["Harvest"])

@router.post("/harvests",response_model=HarvestOut,status_code=201)
def post_harvest(data:HarvestCreate,db:Session=Depends(get_db),_=Depends(require_roles("Admin","Farm Manager","Farmer"))):
    crop=db.get(Crop,data.crop_id)
    if not crop:raise HTTPException(404,"Crop not found")
    if crop.status!="Ready for Harvest":raise HTTPException(400,"Harvest can be created only for Ready for Harvest crops")
    obj=Harvest(**data.model_dump());crop.status="Harvested";db.add(obj);db.commit();db.refresh(obj);return obj

@router.get("/harvests",response_model=list[HarvestOut])
def get_harvests(quality_grade:str|None=None,harvest_date:str|None=None,page:int=1,limit:int=10,db:Session=Depends(get_db),_=Depends(get_current_user)):
    q=db.query(Harvest)
    if quality_grade:q=q.filter(Harvest.quality_grade==quality_grade)
    if harvest_date:q=q.filter(Harvest.harvest_date==harvest_date)
    return q.offset((max(page,1)-1)*limit).limit(min(max(limit,1),100)).all()

@router.get("/crops/{crop_id}/harvest",response_model=list[HarvestOut])
def crop_harvest(crop_id:int,db:Session=Depends(get_db),_=Depends(get_current_user)):
    if not db.get(Crop,crop_id):raise HTTPException(404,"Crop not found")
    return db.query(Harvest).filter(Harvest.crop_id==crop_id).all()
