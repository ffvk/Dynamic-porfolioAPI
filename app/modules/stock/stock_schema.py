from pydantic import BaseModel
from datetime import datetime
from typing import Optional



class GetStockSchema(BaseModel):
    stock_id: Optional[int]
    user_id: Optional[int]
    
    symbol: Optional[str]
    quantity: Optional[float]
    purchase_price: Optional[float]


    is_active: Optional[bool]
    is_deleted: Optional[bool]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    created_by_name: Optional[str]
    updated_by_name: Optional[str]
    created_by: Optional[int]
    updated_by: Optional[int]


class CreateStockSchema(BaseModel):
    user_id: Optional[int]
    symbol: Optional[str]
    quantity: Optional[float]
    purchase_price: Optional[float]
    is_active: Optional[bool] = True
    


class UpdateStockSchema(BaseModel):
    user_id: Optional[int]
    symbol: Optional[str]
    quantity: Optional[float]
    purchase_price: Optional[float]
    is_active: Optional[bool]

    



class DeleteStockSchema(BaseModel):
    message: str
    
    
class Config:
        orm_mode = True
