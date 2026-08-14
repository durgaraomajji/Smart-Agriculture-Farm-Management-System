from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Crop,CropTreatment
from app.schemas.schemas import TreatmentCreate,TreatmentOut
from app.utils.security import get_current_user,require_roles

router=APIRouter(tags=["Fertilizer & Pesticide"])

@router.post("/crop-treatments",response_model=TreatmentOut,status_code=201)
def post_treatment(data:TreatmentCreate,db:Session=Depends(get_db),_=Depends(require_roles("Admin","Farm Manager","Farmer","Field Worker"))):
    if not db.get(Crop,data.crop_id):raise HTTPException(404,"Crop not found")
    obj=CropTreatment(**data.model_dump());db.add(obj);db.commit();db.refresh(obj);return obj

@router.get("/crop-treatments",response_model=list[TreatmentOut])
def get_treatments(page:int=1,limit:int=10,db:Session=Depends(get_db),_=Depends(get_current_user)):
    return db.query(CropTreatment).offset((max(page,1)-1)*limit).limit(min(max(limit,1),100)).all()

@router.get("/crops/{crop_id}/treatments")
def crop_treatments(crop_id:int,db:Session=Depends(get_db),_=Depends(get_current_user)):
    if not db.get(Crop,crop_id):raise HTTPException(404,"Crop not found")
    items=db.query(CropTreatment).filter(CropTreatment.crop_id==crop_id).all()
    return {"crop_id":crop_id,"total_treatment_cost":sum(x.cost for x in items),"treatments":items}
