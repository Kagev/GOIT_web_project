from pydantic import BaseModel


class CommentModel(BaseModel):
	image_name: str
	qr_code: str


class CommentResponse(BaseModel):
	user: CommentModel
