from fastapi import FastAPI
from app.api import auth, posts, categories, admin

app = FastAPI(title="FastAPI Blog Backend")

app.include_router(auth.router)
app.include_router(posts.router)
app.include_router(categories.router)
app.include_router(admin.router)
