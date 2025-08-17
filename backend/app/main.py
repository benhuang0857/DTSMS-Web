from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from routers import auth, users, roles, web_settings, libraries, library_actions, tickets, uploaded_files, file_trackings, autoflows, recipes, processing_steps

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["Content-Type", "Authorization"]
)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(roles.router, prefix="/api/roles", tags=["roles"])
app.include_router(web_settings.router, prefix="/api/web-settings", tags=["web-settings"])
app.include_router(libraries.router, prefix="/api/libraries", tags=["libraries"])
app.include_router(library_actions.router, prefix="/api/library-actions", tags=["library-actions"])
app.include_router(tickets.router, prefix="/api/tickets", tags=["tickets"])
app.include_router(uploaded_files.router, prefix="/api/uploaded-files", tags=["uploaded-files"])
app.include_router(file_trackings.router, prefix="/api/file-trackings", tags=["file-trackings"])
app.include_router(autoflows.router, prefix="/api/autoflows", tags=["autoflows"])
app.include_router(recipes.router, prefix="/api/recipes", tags=["recipes"])
app.include_router(processing_steps.router, prefix="/api/processing-steps", tags=["processing-steps"])

# 確保uploads目錄存在並添加靜態文件服務
os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.get("/")
def read_root():
    return {"message": "DTSMS wrok!"}