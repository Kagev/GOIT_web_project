import asyncio
import uvicorn

from fastapi import FastAPI
from src.routes import auth, image, comments, cloudinary
from front.pages import routes as router_pages
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="PyCraft FastAPI project")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth.router, prefix='/api')
app.include_router(image.router, prefix='/api')
app.include_router(comments.router, prefix='/api')
app.include_router(cloudinary.router, prefix='/api')
# app.include_router(qr.router, prefix='/api')
app.include_router(router_pages.router)





if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
