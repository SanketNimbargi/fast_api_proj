from fastapi import FastAPI

from routers.users import router as user_router
from routers.education import router as education_router
from routers.personalDetail import router as personal_router

from auth import auth_router

app = FastAPI()

app.include_router(auth_router)

app.include_router(user_router)
app.include_router(education_router)
app.include_router(personal_router)