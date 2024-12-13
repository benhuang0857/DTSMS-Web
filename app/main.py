from fastapi import FastAPI
from routers import user, file_upload

app = FastAPI()

# 注册用户相关路由
app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(file_upload.router, prefix="/file_uploads", tags=["file_uploads"])
