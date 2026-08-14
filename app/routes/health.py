from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Crop,CropHealth,Alert
from app.schemas.schemas import HealthCreate,HealthOut
from app.utils.security import get_current_user,require_roles

router=APIRouter(tags=["Crop Health"])

@router.post("/crop-health",response_model=HealthOut,status_code=201)
def post_health(data:HealthCreate,db:Session=Depends(get_db),_=Depends(require_roles("Admin","Farm Manager","Farmer","Field Worker"))):
    if not db.get(Crop,data.crop_id):raise HTTPException(404,"Crop not found")
    obj=CropHealth(**data.model_dump());db.add(obj)
    if data.health_status=="Critical":
        db.add(Alert(crop_id=data.crop_id,message=f"Critical crop health alert for crop {data.crop_id}"))
    db.commit();db.refresh(obj);return obj

@router.get("/crop-health",response_model=list[HealthOut])
def get_health(db:Session=Depends(get_db),_=Depends(get_current_user)):
    return db.query(CropHealth).order_by(CropHealth.inspection_date.desc()).all()

@router.get("/crops/{crop_id}/health-history",response_model=list[HealthOut])
def health_history(crop_id:int,db:Session=Depends(get_db),_=Depends(get_current_user)):
    if not db.get(Crop,crop_id):raise HTTPException(404,"Crop not found")
    return db.query(CropHealth).filter(CropHealth.crop_id==crop_id).order_by(CropHealth.inspection_date.desc()).all()
