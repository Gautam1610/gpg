from fastapi import FastAPI
from sqlalchemy.exc import SQLAlchemyError
from app.db.session import engine
from app.api import routes

app = FastAPI()

@app.on_event("startup")
def startup_event():
    try:
        with engine.connect() as conn:
            print("✅ DB connected successfully!")
    except SQLAlchemyError as e:
        print("❌ DB connection failed:", e)

app.include_router(routes.router)