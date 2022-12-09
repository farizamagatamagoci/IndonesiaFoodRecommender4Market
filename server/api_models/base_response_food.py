from typing import Any
from pydantic import BaseModel

class BaseResponseModelFood(BaseModel):
    Makanan_Terlaris: Any = {}
    Makanan_Rekomendasi: Any ={}