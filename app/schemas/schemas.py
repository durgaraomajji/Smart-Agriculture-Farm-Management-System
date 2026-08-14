from datetime import date
from typing import Optional
from pydantic import BaseModel, EmailStr, Field as PydField, ConfigDict

class UserRegister(BaseModel):
    full_name: str = PydField(min_length=2, max_length=100)
    email: EmailStr
    password: str = PydField(min_length=6)
    role: str = "Farmer"

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    full_name: str
    email: EmailStr
    role: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class FarmCreate(BaseModel):
    farm_name: str = PydField(min_length=2, max_length=150)
    location: str = PydField(min_length=2, max_length=200)
    total_area: float = PydField(gt=0)
    owner_name: str = PydField(min_length=2, max_length=150)
    status: str = "Active"

class FarmUpdate(BaseModel):
    farm_name: Optional[str] = PydField(default=None, min_length=2, max_length=150)
    location: Optional[str] = PydField(default=None, min_length=2, max_length=200)
    total_area: Optional[float] = PydField(default=None, gt=0)
    owner_name: Optional[str] = PydField(default=None, min_length=2, max_length=150)
    status: Optional[str] = None

class FarmOut(FarmCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int

class FieldCreate(BaseModel):
    field_name: str = PydField(min_length=2, max_length=150)
    area: float = PydField(gt=0)
    soil_type: str = PydField(min_length=2)
    irrigation_type: str = PydField(min_length=2)
    status: str = "Active"

class FieldOut(FieldCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    farm_id: int

class CropCreate(BaseModel):
    field_id: int
    crop_name: str = PydField(min_length=2)
    crop_type: str = PydField(min_length=2)
    planting_date: date
    expected_harvest_date: date
    seed_quantity: float = PydField(gt=0)
    status: str = "Planned"

class CropUpdate(BaseModel):
    crop_name: Optional[str] = PydField(default=None, min_length=2)
    crop_type: Optional[str] = PydField(default=None, min_length=2)
    planting_date: Optional[date] = None
    expected_harvest_date: Optional[date] = None
    seed_quantity: Optional[float] = PydField(default=None, gt=0)
    status: Optional[str] = None

class CropOut(CropCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int

class IrrigationCreate(BaseModel):
    field_id: int
    irrigation_date: date
    water_quantity: float = PydField(gt=0)
    duration_minutes: int = PydField(gt=0)
    irrigation_status: str
    remarks: Optional[str] = None

class IrrigationOut(IrrigationCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int

class TreatmentCreate(BaseModel):
    crop_id: int
    product_name: str = PydField(min_length=2)
    product_type: str
    quantity: float = PydField(gt=0)
    applied_date: date
    cost: float = PydField(gt=0)
    remarks: Optional[str] = None

class TreatmentOut(TreatmentCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int

class HealthCreate(BaseModel):
    crop_id: int
    inspection_date: date
    health_status: str
    disease_name: Optional[str] = None
    severity: Optional[str] = None
    remarks: Optional[str] = None

class HealthOut(HealthCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int

class HarvestCreate(BaseModel):
    crop_id: int
    harvest_date: date
    quantity: float = PydField(gt=0)
    unit: str
    quality_grade: str
    storage_location: str

class HarvestOut(HarvestCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int

class SaleCreate(BaseModel):
    harvest_id: int
    buyer_name: str = PydField(min_length=2)
    quantity: float = PydField(gt=0)
    price_per_unit: float = PydField(gt=0)
    sale_date: date
    payment_status: str

class SaleOut(SaleCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    total_amount: float
