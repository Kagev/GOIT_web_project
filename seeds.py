from faker import Faker

from src.database import db, models


fake = Faker('uk_UA')


def main():
    contacts = []

    for _ in range(80):
        first_name, last_name = fake.name().split(' ', maxsplit=1)

        contacts.append(
            models.Contact(
                first_name=first_name,
                last_name=last_name,
                email=fake.email(),
                phone_number=fake.phone_number(),
                birth_date=fake.date_between(start_date='-55y'),
                additional_data=fake.job(),
                user_id=1
            )
        )

    with db.SessionLocal() as session:
        session.add_all(contacts)
        session.commit()


if __name__ == '__main__':
    main()
