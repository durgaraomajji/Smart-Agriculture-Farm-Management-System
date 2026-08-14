from sqlalchemy import func
from app.models.models import Farm, Field, Crop, Harvest, Sale, CropTreatment, Alert

def dashboard(db):
    return {
        "total_farms": db.query(Farm).count(),
        "total_fields": db.query(Field).count(),
        "active_crops": db.query(Crop).filter(Crop.status == "Growing").count(),
        "crops_ready_for_harvest": db.query(Crop).filter(Crop.status == "Ready for Harvest").count(),
        "critical_crop_alerts": db.query(Alert).filter(Alert.status == "Unread").count(),
        "total_harvest_quantity": db.query(func.coalesce(func.sum(Harvest.quantity), 0)).scalar(),
        "total_sales": db.query(Sale).count(),
        "total_revenue": db.query(func.coalesce(func.sum(Sale.total_amount), 0)).scalar(),
        "total_treatment_cost": db.query(func.coalesce(func.sum(CropTreatment.cost), 0)).scalar(),
    }

def farm_revenue(db):
    rows = db.query(Farm.farm_name, func.coalesce(func.sum(Sale.total_amount), 0)).join(Field, Field.farm_id == Farm.id).join(Crop, Crop.field_id == Field.id).join(Harvest, Harvest.crop_id == Crop.id).join(Sale, Sale.harvest_id == Harvest.id).group_by(Farm.id).all()
    return [{"farm_name": name, "revenue": float(revenue)} for name, revenue in rows]

def crop_production(db):
    rows = db.query(Crop.crop_name, func.coalesce(func.sum(Harvest.quantity), 0)).outerjoin(Harvest, Harvest.crop_id == Crop.id).group_by(Crop.id).all()
    return [{"crop_name": name, "production": float(quantity)} for name, quantity in rows]
