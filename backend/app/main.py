from fastapi import FastAPI
from routers import users, file_uploads, logs, reports, roles, automations, actions, auth

app = FastAPI()

app.include_router(logs.router, prefix="/logs", tags=["logs"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(roles.router, prefix="/roles", tags=["roles"])
app.include_router(reports.router, prefix="/reports", tags=["reports"])
app.include_router(file_uploads.router, prefix="/file_uploads", tags=["file_uploads"])
app.include_router(automations.router, prefix="/automations", tags=["automations"])
app.include_router(actions.router, prefix="/actions", tags=["actions"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])

@app.get("/")
def read_root():
    return {"message": "DTSMS wrok!"}