from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.auth.routes import router as auth_router
from app.tasks.routes import router as tasks_router
from app.users.routes import router as users_router

# создаем таблицы в БД
Base.metadata.create_all(bind=engine)

app = FastAPI()

# настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# настройка статики и шаблонов
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# подключаем роуты
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(tasks_router, prefix="/api", tags=["Tasks"])
app.include_router(users_router, prefix="/api", tags=['Users'])

# роуты для страниц
@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/auth", response_class=HTMLResponse)
async def read_auth(request: Request):
    return templates.TemplateResponse("auth.html", {"request": request})

@app.get("/tasks", response_class=HTMLResponse)
async def read_tasks(request: Request):
    return templates.TemplateResponse("tasks.html", {"request": request})

@app.get("/users", response_class=HTMLResponse)
async def read_users(request: Request):
    return templates.TemplateResponse("users.html", {"request": request}) 