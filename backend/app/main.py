from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, users, roles

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["Content-Type", "Authorization"]
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(roles.router, prefix="/roles", tags=["roles"])

@app.get("/")
def read_root():
    return {"message": "DTSMS wrok!"}