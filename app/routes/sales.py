from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Sale,Harvest
from app.schemas.schemas import SaleCreate,SaleOut
from app.utils.security import get_current_user,require_roles

router=APIRouter(tags=["Sales"])

@router.post("/sales",response_model=SaleOut,status_code=201)
def post_sale(data:SaleCreate,db:Session=Depends(get_db),_=Depends(require_roles("Admin","Farm Manager"))):
    harvest=db.get(Harvest,data.harvest_id)
    if not harvest:raise HTTPException(404,"Harvest not found")
    sold=sum(x.quantity for x in db.query(Sale).filter(Sale.harvest_id==harvest.id).all())
    if sold+data.quantity>harvest.quantity:raise HTTPException(400,"Cannot sell more produce than harvested quantity")
    obj=Sale(**data.model_dump(),total_amount=data.quantity*data.price_per_unit)
    db.add(obj);db.commit();db.refresh(obj);return obj

@router.get("/sales",response_model=list[SaleOut])
def get_sales(payment_status:str|None=None,buyer:str|None=None,page:int=1,limit:int=10,db:Session=Depends(get_db),_=Depends(get_current_user)):
    q=db.query(Sale)
    if payment_status:q=q.filter(Sale.payment_status==payment_status)
    if buyer:q=q.filter(Sale.buyer_name.ilike(f"%{buyer}%"))
    return q.offset((max(page,1)-1)*limit).limit(min(max(limit,1),100)).all()

@router.get("/sales/{sale_id}",response_model=SaleOut)
def get_sale(sale_id:int,db:Session=Depends(get_db),_=Depends(get_current_user)):
    obj=db.get(Sale,sale_id)
    if not obj:raise HTTPException(404,"Sale not found")
    return obj
