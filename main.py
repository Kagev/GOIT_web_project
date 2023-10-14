import uvicorn

from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.routes import comments

app = FastAPI()

app.include_router(comments.router, prefix='/api')

@app.get("/api/healthchecker")
def healthchecker(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT 1")).fetchone()
        print(result)
        if result is None:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Database is not configured correctly")
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Error connecting to the database")


if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8000, reload=True)
