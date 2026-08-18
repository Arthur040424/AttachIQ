from fastapi import FastAPI
from routers import auth
from routers import evidence

app = FastAPI()
app.include_router(auth.router)
app.include_router(evidence.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}

