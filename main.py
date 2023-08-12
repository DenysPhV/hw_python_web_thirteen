from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse

from sqlalchemy.orm import Session
from sqlalchemy import text

from src.database.connector import get_db
from src.routes import contacts, notes, auth

app = FastAPI()


@app.get("/", response_class=HTMLResponse, description="Main Page")
async def root(request: Request):
    return {"message": "Welcome to FastAPI homework!"}


@app.get("/api/healthchecker")
def healthchecker(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT 1")).fetchone()
        if result is None:
            raise HTTPException(status_code=500, detail="Database is not configured correctly")
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error connecting to the database")


app.include_router(contacts.router, prefix='/api')
app.include_router(contacts.finder, prefix='/api')
app.include_router(notes.router, prefix='/api')
app.include_router(auth.router, prefix='/api')
