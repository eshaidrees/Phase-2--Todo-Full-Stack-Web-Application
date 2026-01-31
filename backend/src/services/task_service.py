from sqlmodel import Session, select
from typing import List, Optional
from src.models.task import Task, TaskCreate, TaskUpdate
from src.models.user import User
from datetime import datetime
import uuid

class TaskService:
    @staticmethod
    def create_task(session: Session, task_create: TaskCreate, user_id: uuid.UUID) -> Task:
        # Create task object with the user_id from the authenticated user
        db_task = Task(
            title=task_create.title,
            description=task_create.description,
            completed=task_create.completed,
            due_date=task_create.due_date,
            user_id=user_id
        )

        # Add to session and commit
        session.add(db_task)
        session.commit()
        session.refresh(db_task)

        return db_task

    @staticmethod
    def get_tasks_by_user(session: Session, user_id: uuid.UUID, limit: int = 50, offset: int = 0, completed: Optional[bool] = None) -> List[Task]:
        # Build query
        query = select(Task).where(Task.user_id == user_id)

        # Apply filters
        if completed is not None:
            query = query.where(Task.completed == completed)

        # Apply pagination
        query = query.offset(offset).limit(limit)

        # Execute query
        tasks = session.exec(query).all()
        return tasks

    @staticmethod
    def get_task_by_id_and_user(session: Session, task_id: uuid.UUID, user_id: uuid.UUID) -> Optional[Task]:
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        task = session.exec(statement).first()
        return task

    @staticmethod
    def update_task(session: Session, task_id: uuid.UUID, task_update: TaskUpdate, user_id: uuid.UUID) -> Optional[Task]:
        # Get the existing task
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        db_task = session.exec(statement).first()

        if not db_task:
            return None

        # Update the task with the provided values
        update_data = task_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_task, field, value)

        # Update the updated_at timestamp
        db_task.updated_at = datetime.now()

        # Commit changes
        session.add(db_task)
        session.commit()
        session.refresh(db_task)

        return db_task

    @staticmethod
    def delete_task(session: Session, task_id: uuid.UUID, user_id: uuid.UUID) -> bool:
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        db_task = session.exec(statement).first()

        if not db_task:
            return False

        session.delete(db_task)
        session.commit()
        return True

    @staticmethod
    def update_task_completion(session: Session, task_id: uuid.UUID, completed: bool, user_id: uuid.UUID) -> Optional[Task]:
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        db_task = session.exec(statement).first()

        if not db_task:
            return None

        # Update the completion status
        db_task.completed = completed
        db_task.updated_at = datetime.now()

        # Commit changes
        session.add(db_task)
        session.commit()
        session.refresh(db_task)

        return db_task