import requests
import random
import string
import faker
import json

from base_api.get_ingredients_api import GetIngredients
from base_urls import *


def get_sing_up_data():
    fake = faker.Faker()
    email = fake.email()

    return email


def create_new_user_and_return_email_password_name():
    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string

    login_pass = []

    email = get_sing_up_data()
    password = generate_random_string(10)
    name = generate_random_string(10)

    payload = {
        "email": email,
        "password": password,
        "name": name
    }

    response = requests.post(MAIN_URL+CREATE_USER_ENDPOINT, data=payload)

    if response.status_code == 200:
        login_pass.append(email)
        login_pass.append(password)
        login_pass.append(name)

    return response.status_code, response.json(), login_pass


def create_ingredients_list():
    ingredients_list = []
    new_ingredients = GetIngredients(MAIN_URL)
    response = new_ingredients.get_ingredients().json()
    if response.get("success") and "data" in response:
        data = response["data"]
        num_ingredients = random.randint(1, 5)
        random_ingredients = random.sample(data, num_ingredients)
        ingredients_list = [ingredient["_id"] for ingredient in random_ingredients]

    return ingredients_list






