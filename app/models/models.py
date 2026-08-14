from datetime import date, datetime
from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(30), nullable=False, default="Farmer")

class Farm(Base):
    __tablename__ = "farms"
    id = Column(Integer, primary_key=True)
    farm_name = Column(String(150), unique=True, nullable=False)
    location = Column(String(200), nullable=False)
    total_area = Column(Float, nullable=False)
    owner_name = Column(String(150), nullable=False)
    status = Column(String(30), nullable=False, default="Active")
    fields = relationship("Field", back_populates="farm", cascade="all, delete-orphan")

class Field(Base):
    __tablename__ = "fields"
    id = Column(Integer, primary_key=True)
    farm_id = Column(Integer, ForeignKey("farms.id"), nullable=False)
    field_name = Column(String(150), nullable=False)
    area = Column(Float, nullable=False)
    soil_type = Column(String(100), nullable=False)
    irrigation_type = Column(String(100), nullable=False)
    status = Column(String(30), nullable=False, default="Active")
    farm = relationship("Farm", back_populates="fields")
    crops = relationship("Crop", back_populates="field", cascade="all, delete-orphan")

class Crop(Base):
    __tablename__ = "crops"
    id = Column(Integer, primary_key=True)
    field_id = Column(Integer, ForeignKey("fields.id"), nullable=False)
    crop_name = Column(String(150), nullable=False)
    crop_type = Column(String(100), nullable=False)
    planting_date = Column(Date, nullable=False)
    expected_harvest_date = Column(Date, nullable=False)
    seed_quantity = Column(Float, nullable=False)
    status = Column(String(30), nullable=False, default="Planned")
    field = relationship("Field", back_populates="crops")

class Irrigation(Base):
    __tablename__ = "irrigation"
    id = Column(Integer, primary_key=True)
    field_id = Column(Integer, ForeignKey("fields.id"), nullable=False)
    irrigation_date = Column(Date, nullable=False)
    water_quantity = Column(Float, nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    irrigation_status = Column(String(50), nullable=False)
    remarks = Column(Text, nullable=True)

class CropTreatment(Base):
    __tablename__ = "crop_treatments"
    id = Column(Integer, primary_key=True)
    crop_id = Column(Integer, ForeignKey("crops.id"), nullable=False)
    product_name = Column(String(150), nullable=False)
    product_type = Column(String(50), nullable=False)
    quantity = Column(Float, nullable=False)
    applied_date = Column(Date, nullable=False)
    cost = Column(Float, nullable=False)
    remarks = Column(Text, nullable=True)

class CropHealth(Base):
    __tablename__ = "crop_health"
    id = Column(Integer, primary_key=True)
    crop_id = Column(Integer, ForeignKey("crops.id"), nullable=False)
    inspection_date = Column(Date, nullable=False)
    health_status = Column(String(30), nullable=False)
    disease_name = Column(String(150), nullable=True)
    severity = Column(String(50), nullable=True)
    remarks = Column(Text, nullable=True)

class Harvest(Base):
    __tablename__ = "harvests"
    id = Column(Integer, primary_key=True)
    crop_id = Column(Integer, ForeignKey("crops.id"), nullable=False)
    harvest_date = Column(Date, nullable=False)
    quantity = Column(Float, nullable=False)
    unit = Column(String(30), nullable=False)
    quality_grade = Column(String(30), nullable=False)
    storage_location = Column(String(200), nullable=False)

class Sale(Base):
    __tablename__ = "sales"
    id = Column(Integer, primary_key=True)
    harvest_id = Column(Integer, ForeignKey("harvests.id"), nullable=False)
    buyer_name = Column(String(150), nullable=False)
    quantity = Column(Float, nullable=False)
    price_per_unit = Column(Float, nullable=False)
    total_amount = Column(Float, nullable=False)
    sale_date = Column(Date, nullable=False)
    payment_status = Column(String(30), nullable=False)

class Alert(Base):
    __tablename__ = "alerts"
    id = Column(Integer, primary_key=True)
    crop_id = Column(Integer, ForeignKey("crops.id"), nullable=False)
    message = Column(String(300), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String(30), default="Unread")
