from fastapi import Depends, FastAPI, HTTPException
from db.databse import engine, sessionmaker, SessionLocal
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from models import model
from models.model import Customer,Menu, Table, Order, OrderItem
from schemas.shcemas import CustomerSchema ,TableSchema,MenuSchema,OrderSchema, OrderItemSchema


app = FastAPI()
model.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



#Create Customer:

@app.post("/customers", response_model=CustomerSchema)
async def create_customer(customer: CustomerSchema, db: Session = Depends(get_db)):
    new_customer = Customer(**customer.dict())
    db.add(new_customer)
    db.commit()
    return new_customer
 
# Get Customer With Customer ID
@app.get("/customers/{customer_id}", response_model=CustomerSchema)
async def get_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found.")
    return customer

@app.post("/tables", response_model=TableSchema)
async def create_table(table: TableSchema, db: Session = Depends(get_db)):
    new_table = Table(**table.dict())
    db.add(new_table)
    db.commit()
    return new_table



@app.put("/tables/{table_id}/availability")
async def update_table_availability(table_id: int, available: bool, db: Session = Depends(get_db)):
    table = db.query(Table).filter(Table.id == table_id).first()
    if not table:
        raise HTTPException(status_code=404, detail="Table not found.")
    table.available = available
    db.commit()
    return {"message": "Table availability updated successfully."}

@app.post("/menus", response_model=MenuSchema)
async def create_menu_item(menu_item: MenuSchema, db: Session = Depends(get_db)):
    new_menu_item = Menu(**menu_item.dict())
    db.add(new_menu_item)
    db.commit()
    return new_menu_item


@app.post("/orders", response_model=OrderSchema)
async def create_order(order: OrderSchema, db: Session = Depends(get_db)):
    new_order = Order(**order.dict())
    db.add(new_order)
    db.commit()
    return new_order




@app.post("/orders/{order_id}/items", response_model=OrderItemSchema)
async def add_order_item(order_id: int, order_item: OrderItemSchema, db: Session = Depends(get_db)):
    new_order_item = OrderItem(**order_item.dict(), order_id=order_id)
    db.add(new_order_item)
    db.commit()
    return new_order_item



@app.get("/customers/{customer_id}/bill", response_model=float)
async def get_customer_total_bill(customer_id: int, db: Session = Depends(get_db)):
    """
    Calculates and returns the total bill amount for a customer across all their orders.
    """
    orders = db.query(Order).filter(Order.customer_id == customer_id).all()
    total_bill = sum(order.total_amount for order in orders)
    return total_bill



@app.get("/customers")
async def get_all_customers(db: Session = Depends(get_db)):
    """
    Retrieves and returns a list of all customers in the system.
    """
    customers = db.query(Customer).all()
    return customers



@app.get("/menus")
async def get_all_menu_items(db: Session = Depends(get_db)):
    """
    Retrieves and returns a list of all menu
    """
    menu_items = db.query(Menu).all()
    
    return menu_items
