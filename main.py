import uvicorn
import redis.asyncio as redis
from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter
from config import settings
from src.routes import auth, admin, comments, cloudinary, image, qr, users
from front.pages import routes as pages
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="PyCraft FastAPI project")

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.on_event("startup")
async def startup():
	"""
	The startup function is called when the application starts up.
	It's a good place to initialize things that are used by the app, like databases or caches.

	:return: A coroutine, so we need to call it with await

	"""
	await FastAPILimiter.init(
		await redis.Redis(
			host=settings.redis_host,
			port=settings.redis_port,
			# password=settings.redis_password,
			db=0,
			encoding="utf-8",
			decode_responses=True,
		)
	)


app.include_router(auth.router, prefix="/api")
app.include_router(admin.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(image.router, prefix="/api")
app.include_router(comments.router, prefix="/api")
app.include_router(cloudinary.router, prefix="/api")
app.include_router(qr.router, prefix='/api')
app.include_router(pages.router)

if __name__ == "__main__":
	uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
