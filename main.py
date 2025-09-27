from fastapi import FastAPI
from services import auth_service, storage_service
import uvicorn

app = FastAPI(title="Integrated Test Dev - Assignment")

# Auth endpoints under /auth
app.include_router(auth_service.router, prefix="/auth", tags=["auth"])

# Storage endpoints directly under /items, /items/{id}, etc.
app.include_router(storage_service.router, tags=["storage"])

@app.get("/")
def root():
    return {"message": "OK"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
