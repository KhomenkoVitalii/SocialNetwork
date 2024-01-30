from faker import Faker
import random

faker = Faker()


def generate_user_data():
    return {
        'email': faker.email(),
        'phone_number': f"+38098{random.randint(100,999)}{random.randint(10, 99)}00",
        'username': faker.user_name(),
        'first_name': faker.first_name(),
        'last_name': faker.last_name(),
        'password': faker.password()
    }


def generate_user_post():
    return {
        'title': faker.name(),
        'body': faker.text(),
    }
