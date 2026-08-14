from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.models import Crop, Field

ACTIVE_STATUSES = {"Planned", "Growing", "Ready for Harvest"}

def create_crop(db: Session, data):
    field = db.get(Field, data.field_id)
    if not field:
        raise HTTPException(404, "Field not found")
    if field.status != "Active":
        raise HTTPException(400, "Inactive fields cannot be used for cultivation")
    if data.planting_date > data.expected_harvest_date:
        raise HTTPException(400, "Planting date cannot be after harvest date")
    for crop in field.crops:
        if crop.status in ACTIVE_STATUSES and data.planting_date <= crop.expected_harvest_date and data.expected_harvest_date >= crop.planting_date:
            raise HTTPException(409, "Field has an overlapping active crop")
    obj = Crop(**data.model_dump())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

def update_crop(db: Session, crop: Crop, data):
    if crop.status == "Harvested":
        raise HTTPException(400, "Harvested crops cannot be modified")
    values = data.model_dump(exclude_unset=True)
    planting = values.get("planting_date", crop.planting_date)
    harvest = values.get("expected_harvest_date", crop.expected_harvest_date)
    if planting > harvest:
        raise HTTPException(400, "Planting date cannot be after harvest date")
    for k, v in values.items():
        setattr(crop, k, v)
    db.commit(); db.refresh(crop)
    return crop
