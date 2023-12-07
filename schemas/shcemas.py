from pydantic import BaseModel, Field

class CustomerSchema(BaseModel):
    name: str
    email: str | None
    phone: str | None

class MenuSchema(BaseModel):
    name: str
    description: str | None
    price: float


class OrderSchema(BaseModel):
    customer_id: int
    table_id: int
    total_amount: float = Field(default=0.0)

class OrderItemSchema(BaseModel):
    menu_id: int
    quantity: int   


class TableSchema(BaseModel):
    number: int
    capacity: int
    available: bool = True
