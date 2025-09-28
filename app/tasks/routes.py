from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.tasks.models import Task  
from app.tasks.schemas import StatusPatch, TaskBase, TaskRead, TaskUpdate, AssignPatch
from datetime import datetime
from sqlalchemy import case, func
import json

router = APIRouter()

# порядок приоритетов
priority_order = case(
    (func.lower(Task.priority) == "critical", 1),
    (func.lower(Task.priority) == "high", 2),
    (func.lower(Task.priority) == "medium", 3),
    (func.lower(Task.priority) == "low", 4),
    else_=5
)

# подключение к БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post('/tasks', response_model=TaskRead)
async def task_create(task: TaskBase, db: Session = Depends(get_db)):
    try:
        db_task = Task(
            title=task.title,
            description=task.description,
            category=task.category,
            status=task.status,
            priority=task.priority,
            location_id=task.location_id,
            created_by=task.created_by,
            assigned_to=task.assigned_to,
            due_date=task.due_date,
            attachments=task.attachments,
            created_at=datetime.utcnow()
        )

        db.add(db_task)
        db.commit()
        db.refresh(db_task)

        return db_task
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка создания задачи: {str(e)}")



@router.get('/tasks/{id}')
async def task_get(id: int, db: Session = Depends(get_db)):
    get_task = db.query(Task).filter(Task.id == id).first()
    if not get_task:
        raise HTTPException(status_code=404, detail=f'Номера заявки: #{id} нет.')
    return get_task


@router.put('/tasks/{id}', response_model=TaskRead)
async def task_update(id: int, updated: TaskUpdate, db: Session = Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail='Такого ID нет')

    if updated.description is not None:
        db_task.description = updated.description
    if updated.assigned_to is not None:
        db_task.assigned_to = updated.assigned_to
    if updated.attachments is not None:
        db_task.attachments = updated.attachments
    if updated.category is not None:
        db_task.category = updated.category
    if updated.priority is not None:
        db_task.priority = updated.priority
    if updated.status is not None:
        db_task.status = updated.status

    db.commit()
    db.refresh(db_task)

    return db_task


@router.delete('/tasks/{id}')
async def task_delete(id: int, db: Session = Depends(get_db)):
    get_task = db.query(Task).filter(Task.id == id).first()
    if not get_task:
        raise HTTPException(404, 'Такого ИД нема')
    db.delete(get_task)
    db.commit()
    
    return {'Message': f'Task ID[#{id}] Deleted!'}



@router.get("/tasks", response_model=list[TaskRead])
async def list_tasks(db: Session = Depends(get_db)):
    return db.query(Task).order_by(priority_order).all()



@router.patch('/tasks/{id}/status')
async def patch_task(id: int, status: StatusPatch, db: Session = Depends(get_db)):
    patch_status = db.query(Task).filter(Task.id == id).first()
    if not patch_status:
        raise HTTPException(404, 'Not Found!')
    if status.status is not None:
        patch_status.status = status.status
        
    db.add(patch_status)
    db.commit()
    db.refresh(patch_status)
    return {'Message': f'Status under - [ID:{id}] Changed!'}


@router.patch('/tasks/{id}/assign')
async def patch_task(id: int, assign: AssignPatch, db: Session = Depends(get_db)):
    patch_assign = db.query(Task).filter(Task.id == id).first()
    if not patch_assign:
        raise HTTPException(404, 'Not Found!')
    if assign.assigned_to is not None:
        patch_assign.assigned_to = assign.assigned_to
        
    db.add(patch_assign)
    db.commit()
    db.refresh(patch_assign)
    return {'Message': f'Assign under - [ID:{id}] Changed!'}


"""Заявки (основной API)
POST /api/v1/tasks - создание заявки
GET /api/v1/tasks/{id} - получение заявки
PUT /api/v1/tasks/{id} - обновление заявки
DELETE /api/v1/tasks/{id} - удаление заявки
GET /api/v1/tasks - список заявок с фильтрами
PATCH /api/v1/tasks/{id}/status - изменение статуса
PATCH /api/v1/tasks/{id}/assign - назначение исполнителя
____________________________________________________
GET /api/v1/tasks/{id}/history - история изменений
POST /api/v1/tasks/{id}/rating - оценка заявки
"""