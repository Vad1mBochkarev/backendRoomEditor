from app.core.minio import minio_client
from minio import S3Error
import os
import datetime


def upload_3d_model(object_name, file_path, bucket_name='my-test-bucket'):
    if not os.path.exists(file_path):
        print(f"Ошибка: Локальный файл {file_path} не найден!")
        return False
    
    try:
        # 1. Проверяем наличие корзины
        if not minio_client.bucket_exists(bucket_name):
            print(f"Корзина '{bucket_name}' не найдена. Создаем новую...")
            minio_client.make_bucket(bucket_name)
        
        # 2. Проверяем, существует ли объект в MinIO
        try:
            minio_client.stat_object(bucket_name, object_name)
            print(f"Объект '{object_name}' уже существует в корзине '{bucket_name}'. Повторная загрузка не требуется.")
            return True  # Возвращаем True, так как объект уже есть
        except S3Error as stat_err:
            if stat_err.code != "NoSuchKey":
                # Если ошибка не о том, что объект не найден, выводим предупреждение
                print(f"Предупреждение: не удалось проверить наличие объекта '{object_name}': {stat_err}")
        
        # 3. Определение Content-Type (Опционально, но рекомендуется)
        # Для 3D моделей часто используют универсальный бинарный тип
        content_type = "application/octet-stream"
        if file_path.endswith('.gltf'):
            content_type = "model/gltf+json"
        elif file_path.endswith('.glb'):
            content_type = "model/gltf-binary"

        # 4. Загрузка файла
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


def upload_folder(folder_name, local_folder_path, bucket_name='my-test-bucket'):
    """
    Загружает всю папку (все файлы внутри) в MinIO.
    
    :param bucket_name: Имя корзины в MinIO
    :param folder_name: Имя папки в MinIO (например, "Boombox")
    :param local_folder_path: Путь к локальной папке
    :return: True если успешно, False в противном случае
    """
    if not os.path.exists(local_folder_path):
        print(f"Ошибка: Локальная папка {local_folder_path} не найдена!")
        return False
    
    if not os.path.isdir(local_folder_path):
        print(f"Ошибка: {local_folder_path} не является папкой!")
        return False
    
    try:
        # 1. Проверяем наличие корзины
        if not minio_client.bucket_exists(bucket_name):
            print(f"Корзина '{bucket_name}' не найдена. Создаем новую...")
            minio_client.make_bucket(bucket_name)
        
        # 2. Проходим по всем файлам в папке
        for filename in os.listdir(local_folder_path):
            local_file_path = os.path.join(local_folder_path, filename)
            
            # Пропускаем подпапки, загружаем только файлы
            if os.path.isfile(local_file_path):
                # Имя объекта в MinIO: "Boombox/BoomBox.gltf"
                object_name = f"{folder_name}/{filename}"
                
                # Проверяем, существует ли объект в MinIO
                try:
                    minio_client.stat_object(bucket_name, object_name)
                    print(f"Объект '{object_name}' уже существует в корзине '{bucket_name}'. Пропускаем загрузку.")
                    continue
                except S3Error as stat_err:
                    if stat_err.code != "NoSuchKey":
                        # Если ошибка не о том, что объект не найден, выводим предупреждение
                        print(f"Предупреждение: не удалось проверить наличие объекта '{object_name}': {stat_err}")
                
                try:
                    result = minio_client.fput_object(
                        bucket_name=bucket_name,
                        object_name=object_name,
                        file_path=local_file_path
                    )
                    print(f"Файл '{filename}' успешно загружен! Etag: {result.etag}")
                except S3Error as err:
                    print(f"Ошибка при загрузке файла '{filename}': {err}")
                    return False
        
        print(f"Все файлы из папки '{local_folder_path}' успешно загружены в MinIO!")
        return True
        
    except S3Error as err:
        print(f"Критическая ошибка при работе с MinIO: {err}")
        return False


def get_3d_objects_from_minio(object_name, bucket_name='my-test-bucket'):
    try:
        url = minio_client.presigned_get_object(
            bucket_name=bucket_name,
            object_name=object_name,
            expires=datetime.timedelta(hours=1)
        )
        return url
    except S3Error as err:
        print(f"Ошибка при получении файла MinIO {err}")
        return None