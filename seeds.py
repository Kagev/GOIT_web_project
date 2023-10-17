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
                birth_date=fake.date_of_birth(minimum_age=18, maximum_age=55),
                created_at=fake.date_time(),
                confirmed=choice([True, False]),
                role_id=choice([1, 2, 3]),
                password=fake.password(length=8)
            )
            session.add(user)

            user_role = models.UserRole(
                role_name=choice(["admin", "moderator", "user"])
            )
            session.add(user_role)

            photo = models.Photo(
                description=fake.text(),
                created_at=fake.date_time()
            )
            session.add(photo)

        session.commit()


if __name__ == "__main__":
    main()
