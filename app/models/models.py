from datetime import datetime
from typing import Dict, Any
from sqlalchemy import DateTime
from sqlalchemy import Column, Float, Date, ForeignKey, Integer, String, CheckConstraint
from sqlalchemy.orm import relationship

from app.models.database import Base


class FileVersion(Base):
    """
    Модель версии файла.

    Атрибуты:
        id (int): Идентификатор версии файла.
        path_file (str): Путь к файлу.
        created_on (datetime): Дата создания версии файла.
        projects (Relationship): Связь с проектами.

    """
    __tablename__ = 'file_versions'
    id: int = Column(Integer, primary_key=True, index=True)
    created_on: datetime = Column(DateTime(), default=datetime.now)
    projects = relationship('Project', back_populates='file_version')

    # def __repr__(self) -> str:
    #     # return (f"FileVersion(id={self.id}, path_file={self.path_file}, "
    #     #         f"created_on={self.created_on}, projects={self.projects})")
    #     return 'FileVersion'

    def to_json(self):

        return {
            "id": self.id,
            "path_file": self.path_file,
            "created_on": self.created_on
        }


class Project(Base):
    """
    Модель проекта.

    Атрибуты:
        id (int): Идентификатор проекта.
        code (int): Код проекта.
        name (str): Название проекта.
        values (Relationship): Связь с значениями.
        file_version_id (int): Идентификатор версии файла, к которой относится проект.
        file_version (Relationship): Связь с версией файла.

    """
    __tablename__ = 'projects'
    __table_args__ = (
        CheckConstraint('LENGTH(name) >= 1 AND LENGTH(name) <= 100'),
    )
    id: int = Column(Integer, primary_key=True, index=True)
    code: int = Column(Integer, index=True, nullable=False)
    name: str = Column(String(100))
    values = relationship('Value', back_populates="project")
    file_version_id: int = Column(Integer, ForeignKey('file_versions.id'))
    file_version = relationship('FileVersion', back_populates='projects')

    # def __repr__(self) -> str:
    #     # return f'Project(id={self.id}, code={self.code}, file_version_id={self.file_version_id})'
    #     return 'Project'

    async def to_json(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "code": self.code,
            "project": self.name,
            "file_version_id": self.file_version_id,
            "values": [await val.to_json() for val in self.values]
        }


class Value(Base):
    """
    Модель значений проекта.

    Атрибуты:
        id (int): Идентификатор значения.
        project_id (int): Идентификатор проекта.
        date (Date): Дата достигнутного значения.
        plan_value (float): Плановое значение.
        fact_value (float): Фактическое значение.
        project (Relationship): Связь с проектом.

    """
    __tablename__ = 'values'
    id: int = Column(Integer, primary_key=True, index=True)
    project_id: int = Column(Integer, ForeignKey('projects.id'))
    date: Date = Column(Date)
    plan_value: float = Column(Float, nullable=True)
    fact_value: float = Column(Float, nullable=True)
    project = relationship('Project', back_populates="values")

    # def __repr__(self) -> str:
    #     # return (f'Value(id={self.id}, project_id={self.project_id}, date={self.date}, '
    #     #         f'plan_value={self.plan_value}, fact_value={self.fact_value})')
    #     return 'Value'

    async def to_json(self):
        return {
            "id": self.id,
            "date": self.date,
            "plan_value": self.plan_value,
            "fact_value": self.fact_value
        }
