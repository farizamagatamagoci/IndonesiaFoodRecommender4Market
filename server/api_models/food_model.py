from pydantic import BaseModel

class FoodModel(BaseModel):
    nomor: int
    makanan: str