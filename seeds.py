import requests
from random import choice, sample, randint
from faker import Faker
from src.database import db, models
from src.services.auth import Auth

fake = Faker("uk_UA")
auth = Auth()
url_local = 'http://0.0.0.0:8000/'
url_cloud = "https://pycrafters-project-pycrafters.koyeb.app"


def main():
    with db.SessionLocal() as session:
        for _ in range(10):
            url = f"{url_local}/api/auth/signup"

            username = fake.user_name()
            email = fake.email()
            password = fake.password(length=8)

            payload = {
                "username": username,
                "email": email,
                "password": password
            }
            response = requests.post(url, json=payload)

            print(response.status_code)
            print(response.json())

            user = models.User(
                created_at=fake.date_time(),
                role=choice(["admin", "moderator", "user"]),
            )
            session.add(user)

        tags = set()
        while len(tags) < 5:
            tag_name = fake.word()
            if tag_name not in tags:
                tags.add(tag_name)

        for tag_name in tags:
            tag = models.Tag(name=tag_name)
            session.add(tag)

        session.commit()

        images = session.query(models.Image).all()
        tags = session.query(models.Tag).all()
        for image in images:
            tags_to_add = sample(tags, k=randint(1, 3))
            for tag in tags_to_add:
                image_tag = models.ImageTagAssociation(image_id=image.id, tag_id=tag.id)
                session.add(image_tag)

        session.commit()

        users = session.query(models.User).all()
        images = session.query(models.Image).all()
        for _ in range(50):
            comment = models.Comment(
                content=fake.text(max_nb_chars=255),
                user_id=randint(1, 10),
                image_id=randint(1, 20)
            )
            session.add(comment)

        session.commit()


if __name__ == "__main__":
    main()
