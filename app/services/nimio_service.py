from app.core.minio import minio_client
from minio.error import S3Error
import os


def upload_3d_model(bucket_name, object_name, file_path):
    if not os.path.exists(file_path):
        print(f"Ошибка: Локальный файл {file_path} не найден!")
        return False
    
    try:
        # 1. Проверяем наличие корзины
        if not minio_client.bucket_exists(bucket_name):
            print(f"Корзина '{bucket_name}' не найдена. Создаем новую...")
            minio_client.make_bucket(bucket_name)
        
        # 2. Определение Content-Type (Опционально, но рекомендуется)
        # Для 3D моделей часто используют универсальный бинарный тип
        content_type = "application/octet-stream" 
        if file_path.endswith('.gltf'):
            content_type = "model/gltf+json"
        elif file_path.endswith('.glb'):
            content_type = "model/gltf-binary"

        # 3. Загрузка файла
        print(f"Начинаем загрузку файла '{file_path}'...")
        result = minio_client.fput_object(
            bucket_name=bucket_name,
            object_name=object_name,
            file_path=file_path,
            content_type=content_type
        )
        
        print(f"Успех! 3D-модель загружена. Идентификатор версии (Etag): {result.etag}")
        return True

    except S3Error as err:
        print(f"Критическая ошибка при работе с MinIO: {err}")
        return False
    
