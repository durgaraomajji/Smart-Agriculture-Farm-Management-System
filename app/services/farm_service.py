from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.models import Farm, Field

def create_farm(db: Session, data):
    if db.query(Farm).filter(Farm.farm_name == data.farm_name).first():
        raise HTTPException(409, "Farm name already exists")
    obj = Farm(**data.model_dump())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

def add_field(db: Session, farm_id: int, data):
    farm = db.get(Farm, farm_id)
    if not farm:
        raise HTTPException(404, "Farm not found")
    if farm.status != "Active":
        raise HTTPException(400, "Fields cannot be added to an inactive farm")
    used = sum(f.area for f in farm.fields)
    if used + data.area > farm.total_area:
        raise HTTPException(400, f"Field area exceeds available farm area. Available: {farm.total_area-used}")
    if any(f.field_name.lower() == data.field_name.lower() for f in farm.fields):
        raise HTTPException(409, "Field name already exists in this farm")
    obj = Field(farm_id=farm_id, **data.model_dump())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj
