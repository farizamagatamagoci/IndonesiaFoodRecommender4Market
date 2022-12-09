from typing import Any
from pydantic import BaseModel

class BaseResponseModelDiabetesFood(BaseModel):
    Status_Diabetes: Any ={}
    Makanan_Terfavorit: Any = {}
    Makanan_Rekomendasi: Any ={}