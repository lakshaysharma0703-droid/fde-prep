# from fastapi import FastAPI
# from pydantic import BaseModel
# from typing import List

# app = FastAPI()

# class Tea(BaseModel):
#     id: int
#     name: str
#     origin: str

# teas : List[Tea] = []

# @app.get("/")
# def read_root():
#     return {"message": "Welcome to my project"}

# @app.get("/teas")
# def get_teas():
#     return teas

# @app.post("/teas")
# def add_tea(tea:Tea):
#     teas.append(tea)
#     return teas

# @app.put("teas/{tea_id}")
# def update_tea(tea_id: int, updated_tea:Tea):
#     for index, tea in enumerate(teas):
#         if tea.id == tea_id:
#             teas[index] = updated_tea
#             return updated_tea
#     return {"Error":"Tea not found"}

# @app.delete("/teas/{tea_id}")
# def delete_tea(tea_id: int):
#     for index,tea in enumerate(teas):
#         if tea.id == tea_id:
#             deleted = teas.pop(tea_id)
#             return deleted
#     return {"Error":"Tea id not found"}


from fastapi import FastAPI
from pydantic import Field,BaseModel

app = FastAPI(title="Prep API")

@app.get("/hello")
def hello():
    return {"msg": "Hii"}

@app.get("/hello/{name}")
def hello_name(name: str, shout: bool = False):
    message = f"Hello {name}"
    return {"Msg": message.upper() if shout else message}

class LineItem(BaseModel):
    description:str
    qty: int = Field(gt=0)
    unit_price: float = Field(gt=0)

class InvoiceRequest(BaseModel):
    vendor: str
    gst_rate: float = Field(default=0.18,ge=0,le=0.28)
    items: list[LineItem]

@app.post("/invoices")
def create_invoice(invoice: InvoiceRequest):   # request body parsed and validated automatically
    subtotal = sum(item.qty * item.unit_price for item in invoice.items)
    gst = round(subtotal * invoice.gst_rate, 2)
    return {
        "vendor": invoice.vendor,
        "subtotal": subtotal,
        "gst": gst,
        "total": round(subtotal + gst, 2),
    }
