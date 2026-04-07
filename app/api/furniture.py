from fastapi import APIRouter
from uuid import UUID, uuid4
from app.api.dtos import FurnitureResponse,  CategoryResponse

router = APIRouter()

# получить категории мебели
@router.get("/categories")
def get_categories() -> list[CategoryResponse]:
    ...

# полуить всю медель
@router.get("/furniture")
def get_all_furniture() -> list[FurnitureResponse]:
    ...

# получить мебель по айди
@router.get("/furniture/{id}")
def get_futniture_by_id(id: UUID) -> FurnitureResponse:
    ...