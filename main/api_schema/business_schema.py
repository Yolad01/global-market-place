from ninja import Schema, ModelSchema, Form
from main.models import Order
from .user_schema import UserSchema
from datetime import datetime



class OrderSchema(Schema):
    skilla: UserSchema
    client: UserSchema
    notification: int | None
    paid: bool
    order_no: int
    gig_desc: str
    delivery: int
    price: int
    accepted: bool
    completed: bool
    order_created: datetime



class CreateOrderSchema(Schema):
    gig_desc: str = Form(...)
    delivery: int = Form(...)
    price: int = Form(...)


