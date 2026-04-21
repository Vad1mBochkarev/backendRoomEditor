from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from uuid import UUID, uuid4

from app.models import Object3D, Object3DCategory
from app.api.dtos import Object3DResponse, CategoryResponse
from app.core.database import get_db

router = APIRouter()

# получить категории 3D объектов
@router.get("/categories")
def get_categories(db: Session = Depends(get_db)) -> list[CategoryResponse]:
    # Выполняем запрос к БД: получаем все категории 3D объектов
    categories = db.query(Object3DCategory).all()
    # Преобразуем результат в список Pydantic моделей для ответа
    return [CategoryResponse(id=cat.id, name=cat.name) for cat in categories]

# получить все 3D объекты
@router.get("/3d-objects")
def get_all_3d_objects(data: Object3DResponse, db: Session = Depends(get_db)) -> list[Object3DResponse]:
    # Выполняем запрос к БД: получаем 3D объект по ID из запроса
    object_3d = db.query(Object3D).filter(Object3D.id == data.id).first()
    # Возвращаем найденный 3D объект
    return object_3d

# получить 3D объект по айди
@router.get("/3d-objects/{id}")
def get_3d_object_by_id(id: UUID, db: Session = Depends(get_db)) -> Object3DResponse:
    # Выполняем запрос к БД: ищем 3D объект по ID
    object_3d = db.query(Object3D).filter(Object3D.id == id).first()
    # Если 3D объект не найден — выбрасываем 404 ошибку
    if not object_3d:
        raise HTTPException(status_code=404, detail="3D объект не найден")
    # Возвращаем объект 3D (Pydantic схема Object3DResponse)
    return Object3DResponse(
        id=object_3d.id,
        name=object_3d.name,
        category_id=object_3d.category_id,
        file_size=object_3d.file_size,
        file_url=object_3d.file_url
    )