from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.analytics_service import dashboard,farm_revenue,crop_production
from app.utils.security import get_current_user

router=APIRouter(prefix="/dashboard",tags=["Dashboard & Reports"])

@router.get("")
def get_dashboard(db:Session=Depends(get_db),_=Depends(get_current_user)):
    return dashboard(db)

@router.get("/farm-wise-revenue")
def get_farm_revenue(db:Session=Depends(get_db),_=Depends(get_current_user)):
    return farm_revenue(db)

@router.get("/crop-wise-production")
def get_crop_production(db:Session=Depends(get_db),_=Depends(get_current_user)):
    return crop_production(db)
