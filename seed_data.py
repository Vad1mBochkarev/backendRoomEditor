from sqlalchemy.orm import Session
from app.models import Object3D, Object3DCategory
from uuid import UUID, uuid4

def seed_3d_object_categories(db: Session):
    """Добавление примеров категорий 3D объектов в базу данных"""
    categories_data = [
        {"id": UUID('c1a5c1d4-3d4b-4e5f-9b4a-5d6e7f8a9b0c'), "name": "Столы"},
        {"id": UUID('d2b6d2e5-4e5c-5f6a-0c5b-6e7f8a9b0c1d'), "name": "Стулья"},
        {"id": UUID('e3c7e3f6-5f6d-6a7b-1d6c-7f8a9b0c1d2e'), "name": "Шкафы"},
        {"id": UUID('f4d8f4a7-6a7e-7b8c-2e7d-8a9b0c1d2e3f'), "name": "Кровати"},
        {"id": UUID('a5e9a5b8-7b8f-8c9d-3f8e-9b0c1d2e3f4a'), "name": "Диваны"}
    ]
    
    for category_data in categories_data:
        # Проверяем, существует ли категория с таким ID
        existing_category = db.query(Object3DCategory).filter(Object3DCategory.id == category_data["id"]).first()
        if not existing_category:
            # Создаем новую категорию
            category = Object3DCategory(
                id=category_data["id"],
                name=category_data["name"]
            )
            db.add(category)
    
    db.commit()

def seed_3d_objects(db: Session):
    """Добавление примеров 3D объектов в базу данных с пустым file_url"""
    objects_3d_data = [
        {
            "id": UUID('a1b2c3d4-e5f6-7890-abcd-ef1234567890'),
            "name": "Обеденный стол",
            "category_id": UUID('c1a5c1d4-3d4b-4e5f-9b4a-5d6e7f8a9b0c'),  # Столы
            "file_size": 1024000,
            "file_url": ""  # Пустое значение
        },
        {
            "id": UUID('b2c3d4e5-f678-90ab-cdef-1234567890ab'),
            "name": "Офисное кресло",
            "category_id": UUID('d2b6d2e5-4e5c-5f6a-0c5b-6e7f8a9b0c1d'),  # Стулья
            "file_size": 512000,
            "file_url": ""  # Пустое значение
        },
        {
            "id": UUID('c3d4e5f6-7890-abcd-ef12-34567890abcd'),
            "name": "Книжный шкаф",
            "category_id": UUID('e3c7e3f6-5f6d-6a7b-1d6c-7f8a9b0c1d2e'),  # Шкафы
            "file_size": 2048000,
            "file_url": ""  # Пустое значение
        },
        {
            "id": UUID('d4e5f678-90ab-cdef-1234-567890abcdef'),
            "name": "Двуспальная кровать",
            "category_id": UUID('f4d8f4a7-6a7e-7b8c-2e7d-8a9b0c1d2e3f'),  # Кровати
            "file_size": 1536000,
            "file_url": ""  # Пустое значение
        },
        {
            "id": UUID('e5f67890-abcd-ef12-3456-7890abcdef12'),
            "name": "Угловой диван",
            "category_id": UUID('a5e9a5b8-7b8f-8c9d-3f8e-9b0c1d2e3f4a'),  # Диваны
            "file_size": 3072000,
            "file_url": ""  # Пустое значение
        }
    ]
    
    for item_data in objects_3d_data:
        # Проверяем, существует ли 3D объект с таким ID
        existing_object = db.query(Object3D).filter(Object3D.id == item_data["id"]).first()
        if not existing_object:
            # Создаем новый 3D объект
            object_3d = Object3D(
                id=item_data["id"],
                name=item_data["name"],
                category_id=item_data["category_id"],
                file_size=item_data["file_size"],
                file_url=item_data["file_url"]  # Пустое значение
            )
            db.add(object_3d)
    
    db.commit()

def seed_database(db: Session):
    """Заполнение базы данных примерами"""
    print("Заполнение базы данных примерами...")
    
    # Добавляем категории 3D объектов
    seed_3d_object_categories(db)
    print("Категории 3D объектов добавлены")
    
    # Добавляем 3D объекты
    seed_3d_objects(db)
    print("Примеры 3D объектов добавлены")
    
    print("База данных успешно заполнена!")

if __name__ == "__main__":
    # Этот блок кода будет выполнен только при прямом запуске скрипта
    # Он требует дополнительной настройки для подключения к базе данных
    print("Этот скрипт предназначен для использования через FastAPI приложение")