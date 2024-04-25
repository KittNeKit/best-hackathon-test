from typing import TypeVar, Generic
from dataclasses import dataclass
from uuid import UUID
import math

from sqlalchemy.orm import Session

from app.routers.request_task.model import RequestTask
from app.routers.request_task.schema import RequestTaskCreateSchema
from app.routers.user.model import User

T = TypeVar("T")


@dataclass
class PaginatedResult(Generic[T]):
    items: list[T]
    has_next: bool
    has_prev: bool
    current_page: int
    current_limit: int


class RequestTaskCRUD:
    @staticmethod
    def get_request_tasks(db: Session, page: int, limit: int):
        offset = (page - 1) * limit

        tasks = db.query(RequestTask).all()
        task_count = len(tasks)
        page_count = int(math.ceil(task_count / limit))

        items = tasks[offset:offset + limit]

        return PaginatedResult(
            items=items,
            current_page=page,
            current_limit=limit,
            has_prev=page > 1,
            has_next=page < page_count
        )

    @staticmethod
    def get_request_task_by_id(pk: UUID, db: Session):
        return db.query(RequestTask).filter_by(id=pk).first()

    @staticmethod
    def create_request_task(data: RequestTaskCreateSchema, creator: User, db: Session):
        request_task = RequestTask(
            name=data.name,
            description=data.description,
            creator_id=creator.id,
            priority_id=data.priority_id,
        )
        db.add(request_task)
        db.commit()
        db.refresh(request_task)

        return request_task
