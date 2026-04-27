from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from uuid import UUID

from app.models import Object3D, Object3DCategory
from app.api.dtos import Object3DResponse, CategoryResponse
from app.core.database import get_db

from app.services.minio_services import upload_3d_model, upload_folder, get_3d_objects_from_minio

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
def get_all_3d_objects(db: Session = Depends(get_db)) -> list[Object3DResponse]:
    # Выполняем запрос к БД: получаем все 3D объекты
    objects_3d = db.query(Object3D).all()
    # Возвращаем список 3D объектов
    return [
        Object3DResponse(
            id=obj.id,
            name=obj.name,
            category_id=obj.category_id,
            file_size=obj.file_size,
            file_url=obj.file_url
        )
        for obj in objects_3d
    ]

# получить 3D объект по айди
@router.get("/3d-objects/{id}")
def get_3d_object_by_id(id: UUID, db: Session = Depends(get_db)) -> Object3DResponse:
    # Выполняем запрос к БД: ищем 3D объект по ID
    object_3d = db.query(Object3D).filter(Object3D.id == id).first()
    # Если 3D объект не найден — выбрасываем 404 ошибку
    if not object_3d:
        raise HTTPException(status_code=404, detail="3D объект не найден")
    
    # Подготавливаем ссылку на скачивание модели
    generated_url = get_3d_objects_from_minio(object_3d.name)
    if generated_url is None:
        raise HTTPException(status_code=500, detail="Не удалось получить ссылку на 3D модель")

    # Возвращаем объект 3D (Pydantic схема Object3DResponse)
    return Object3DResponse(
        id=object_3d.id,
        name=object_3d.name,
        category_id=object_3d.category_id,
        file_size=object_3d.file_size,
        file_url=generated_url
    )