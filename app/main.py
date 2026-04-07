from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from app.core.database import engine
from app.models import Base
from app.api.status import router as api_status
from app.api.users import router as users_router
from app.api.furniture import router as furniture_router
from app.api.projects import router as progects_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Room Editor API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_status)
app.include_router(users_router)
app. include_router(furniture_router)
app.include_router(progects_router)










# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from app.api.status import router as api_router
# from typing import List, Optional
# from datetime import datetime
# from sqlalchemy import ForeignKey, String, Float, DateTime, INTEGER
# from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
# from sqlalchemy import create_engine, func

# engine = create_engine("postgresql://postgres:postgres@localhost:5432/RoomEditor", echo=True)

# class Base(DeclarativeBase):
#     pass

# class User(Base):
#     __tablename__ = 'users'

#     id: Mapped[int] = mapped_column(INTEGER, primary_key=True)
#     login: Mapped[str] = mapped_column(String(30), unique=True, index=True)
#     password: Mapped[str] = mapped_column(String(60))
#     created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

#     projects: Mapped[list["Project"]] = relationship(back_populates="user")

# class Project(Base):
#     __tablename__ = 'projects'
    
#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str] = mapped_column(String(30))
#     description: Mapped[Optional[str]] = mapped_column(String(200))
#     created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    
#     user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
#     user: Mapped["User"] = relationship(back_populates="projects")
    
#     items: Mapped[list["ProjectItem"]] = relationship(back_populates="project", cascade="all, delete-orphan")

# class ProjectItem(Base):
#     __tablename__ = 'project_items'
    
#     id: Mapped[int] = mapped_column(primary_key=True)
#     x: Mapped[float] = mapped_column()
#     y: Mapped[float] = mapped_column()
#     z: Mapped[float] = mapped_column()
#     rotation: Mapped[float] = mapped_column()
    
#     project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
#     project: Mapped["Project"] = relationship(back_populates="items")

#     furniture_id: Mapped[int] = mapped_column(ForeignKey('furniture.id'))
#     furniture: Mapped["Furniture"] = relationship(back_populates="project_items") 

# class Furniture(Base):
#     __tablename__ = "furniture"

#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str] = mapped_column(String())
#     file_size: Mapped[int] = mapped_column()
#     file_url: Mapped[str] = mapped_column(String)

#     category_id: Mapped[int] = mapped_column(ForeignKey("furniture_categories.id"))
#     category: Mapped["FurnitureCategories"] = relationship(back_populates="furniture")

#     project_items: Mapped[list["ProjectItem"]] = relationship(back_populates="furniture")

# class FurnitureCategories(Base):
#     __tablename__ = "furniture_categories"

#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str] = mapped_column(String(60))

#     furniture: Mapped[list["Furniture"]] = relationship(back_populates="category")


# Base.metadata.create_all(engine)

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:5174"],
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# app.include_router(api_router)