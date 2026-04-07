from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.api.dtos import UserCreate, UserResponse, UserBase
from app.models import User
from app.core.database import get_db

router = APIRouter()


# вход пользователя
@router.post("/auth/login")
def login_user(data: UserBase, db: Session = Depends(get_db)) -> UserResponse:
    # Выполняем запрос к БД: ищем пользователя по логину
    user = db.query(User).filter(User.login == data.login).first()
    #  Если пользователь не найден — выбрасываем 401 ошибку
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль"
        )

    #  Возвращаем объект пользователя (Pydantic схема UserResponse отфильтрует лишнее, например, пароль)
    return user


# регисрация нового пользователя
@router.post("/auth/register")
def register_user(data: UserCreate, db: Session = Depends(get_db)) -> UserResponse:

    # проверка есть ли пользователь с таким логином
    existing_user = db.query(User).filter(User.login == data.login).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким логином уже существует"
        )
    
    # создание пользователя
    new_user = User(login=data.login, password=data.password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user



# # получить данные текущего пользователя
# @router.get("/users/me")
# def get_user() -> UserResponse:
#     ...








