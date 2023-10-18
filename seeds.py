from random import choice
from faker import Faker
from src.database import db, models

fake = Faker("uk_UA")


def main():
    with db.SessionLocal() as session:
        for _ in range(10):
            first_name, last_name = fake.name().split(" ", maxsplit=1)

            user = models.User(
                username=fake.user_name(),
                email=fake.email(),
                created_at=fake.date_time(),
                role=choice(["admin", "moderator", "user"]),
                password=fake.password(length=8)
            )
            session.add(user)

        session.commit()


if __name__ == "__main__":
    main()
