from random import choice
from faker import Faker
from src.database import db, models

fake = Faker("uk_UA")


def main():
    users = []

    for _ in range(80):
        first_name, last_name = fake.name().split(" ", maxsplit=1)

        users.append(
            models.User(
                username=fake.user_name(),
                email=fake.email(),
                birth_date=fake.date_of_birth(minimum_age=18, maximum_age=55),
                created_at=fake.date_time(),
                confirmed=choice([True, False]),
                role_id=choice([1, 2, 3]),
                password=fake.password(length=8)
            )
        )

    with db.SessionLocal() as session:
        session.add_all(users)
        session.commit()


if __name__ == "__main__":
    main()
