from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Irrigation,Field,Crop
from app.schemas.schemas import IrrigationCreate,IrrigationOut
from app.utils.security import get_current_user,require_roles

router=APIRouter(tags=["Irrigation"])

@router.post("/irrigation",response_model=IrrigationOut,status_code=201)
def post_irrigation(data:IrrigationCreate,db:Session=Depends(get_db),_=Depends(require_roles("Admin","Farm Manager","Field Worker"))):
    field=db.get(Field,data.field_id)
    if not field:raise HTTPException(404,"Field not found")
    if field.status!="Active":raise HTTPException(400,"Irrigation requires an active field")
    active=db.query(Crop).filter(Crop.field_id==field.id,Crop.status.in_(["Planned","Growing","Ready for Harvest"])).first()
    if not active:raise HTTPException(400,"Irrigation can be recorded only for active crops")
    obj=Irrigation(**data.model_dump());db.add(obj);db.commit();db.refresh(obj);return obj

@router.get("/irrigation",response_model=list[IrrigationOut])
def get_irrigation(page:int=1,limit:int=10,db:Session=Depends(get_db),_=Depends(get_current_user)):
    return db.query(Irrigation).order_by(Irrigation.irrigation_date.desc()).offset((max(page,1)-1)*limit).limit(min(max(limit,1),100)).all()

@router.get("/fields/{field_id}/irrigation",response_model=list[IrrigationOut])
def field_irrigation(field_id:int,db:Session=Depends(get_db),_=Depends(get_current_user)):
    if not db.get(Field,field_id):raise HTTPException(404,"Field not found")
    return db.query(Irrigation).filter(Irrigation.field_id==field_id).order_by(Irrigation.irrigation_date.desc()).all()
