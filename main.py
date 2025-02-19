from fastapi import FastAPI
from routes.auth_routes import router as auth_router

app = FastAPI()

# Register Routes
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])

@app.get("/")
def home():
    return {"message": "Welcome to Realtime Code Editor API"}
