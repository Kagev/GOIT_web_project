import httpx
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from src.database.connection import SessionLocal
from src.database.models import Comment, User, Image

router = APIRouter(prefix="/pages", tags=["Pages"])

templates = Jinja2Templates(directory="front/templates")

url_local = "http://0.0.0.0:8000"
url_cloud = "https://pycrafters-project-pycrafters.koyeb.app"


@router.get("/base")
@router.get("/index")
@router.get("/home")
def get_base_pages(request: Request):
	session: Session = SessionLocal()
	users = session.query(User).all()
	images = session.query(Image).all()
	comments = session.query(Comment).all()
	lights = []
	for image in images:
		image_comments = [
			comment for comment in comments if comment.image_id == image.id
		]
		light = {
			"image_name": image.image_name,
			"path": image.path,
			"description": image.description,
			"comments": image_comments,
		}
		lights.append(light)
	return templates.TemplateResponse(
		"base.html", {"request": request, "lights": lights}
	)


@router.get("/users")
def get_base_pages(request: Request):
	return templates.TemplateResponse("base.html", {"request": request})


@router.get("/my_account")
def get_user_account():
	user_info = {
		"username": "example_user",
		"email": "user@example.com",
		"lights": ["light1", "light2", "light3"],
	}
	return user_info


@router.get("/login")
async def login(username: str, password: str):
	async with httpx.AsyncClient() as client:
		response = await client.post(
			f"{url_local}/auth/login",
			json={"username": username, "password": password},
		)
		return response.json()
#
# @router.get("/logout")
# async def logout():
# 	async with httpx.AsyncClient() as client:
# 		response = await client.get(f"{url_local}/auth/logout")
# 		return response.json()
#
#
# @router.get("/singing")
# async def register(username: str, email: str, password: str):
# 	async with httpx.AsyncClient() as client:
# 		response = await client.post(
# 			f"{url_local}/auth/signup",
# 			json={"username": username, "email": email, "password": password}, timeout=30
# 		)
# 		return response.json()
#
#
# async def main():
# 	await login("example_user", "password123")
# 	await logout()
# 	await register("new_user", "new_user@example.com", "new_password123")
#
#
# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())
