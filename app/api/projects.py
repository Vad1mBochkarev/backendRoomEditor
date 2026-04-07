from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.database import get_db
from app.api.dtos import ProjectResponse, ProjectCreate

router = APIRouter()

# получить все проекты пользователя
@router.get("/projects")
def get_projects(db: Session = Depends(get_db)) -> list[ProjectResponse]:
    ...

# создать проект
@router.post("/projects/create")
def create_project(data: ProjectCreate, db: Session = Depends(get_db)) -> ProjectResponse:
    ...

# изменить проект (название, описание)
@router.patch("/projects/{id}")
def update_project(id: UUID, data: ProjectCreate, db: Session = Depends(get_db)) -> ProjectResponse:
    ...

# удалить проект
@router.delete("/projects/{id}")
def delete_project(id: UUID, db: Session = Depends(get_db)):
    ...