import json
import random
import requests
from utils import generate_user_data, generate_user_post
import logging

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)


class Bot:
    """
    Object of this bot demonstrate functionalities of the system according to defined rules. This bot
    read rules from a config file

    to run this bot:
    1. environment must be activated
    2. server must be running
    3. run code line 'python bot/automated_bot.py'
    """

    def __init__(self, config_file, base_url):
        with open(config_file, 'r') as file:
            self.config = json.load(file)
        self.base_url = base_url
        self.tokens = {}  # Dictionary to store user tokens
        self.user_unique_identifiers = {}  # Dictionary to store users unique identifiers
        self.post_unique_identifiers = {}  # Dictionary to store posts unique identifiers

    def simulate_activity(self):
        for user_id in range(self.config['number_of_users']):
            user_data = generate_user_data()
            post_data = generate_user_post()
            self.signup_user(user_data)
            self.create_posts(user_data, post_data)
            self.like_posts(user_data)
            print('\n\n\n')

    def signup_user(self, user_data):
        url = f"{self.base_url}/api/v1/auth/users/"
        response = requests.post(url, json=user_data)

        if response.status_code == 201:
            logger.info(
                f"User {user_data['username']} signed up successfully.")
            self.user_unique_identifiers[user_data['username']] = response.json()[
                'id']
            logger.info(
                f"User {user_data['username']} id stored successfully.")
            self.sign_in_user(user_data)
        else:
            logger.critical(f"Failed to sign up user {user_data['username']}.")
            logger.info(f"Get {response.status_code} status code")

    def sign_in_user(self, user_data):
        url = f"{self.base_url}/api/v1/auth/jwt/create/"
        response = requests.post(url, data={'email': user_data.get(
            'email'), 'password': user_data.get('password')})

        if response.status_code == 200:
            self.tokens[user_data['username']] = response.json()['access']
            logger.info(
                f"Stored {user_data.get('username')}'s token successfully!")
        else:
            logger.warning(f"Failed to sign in {user_data['username']}!")
            logger.warning(f"Got {response.status_code} status code")

    def create_posts(self, user_data, post_data):
        token = self.tokens.get(user_data['username'])

        if token:
            num_posts = random.randint(1, self.config['max_posts_per_user'])
            for _ in range(num_posts):
                url = f"{self.base_url}/api/posts/"
                headers = {'Authorization': f'JWT {token}'}
                data = {"title": post_data.get('title'), "body": post_data.get('body'),
                        "user": self.user_unique_identifiers.get(user_data['username'])}

                response = requests.post(url, headers=headers, json=data)

                if response.status_code == 201:
                    self.post_unique_identifiers[user_data['username']] = response.json()[
                        'id']
                    logger.info(
                        f"User {user_data['username']} created post successfully.")
                else:
                    logger.warning(
                        f"Failed to create post by user {user_data['username']}.")
        else:
            logger.warning(
                f"No token found for user {user_data['username']}. Unable to create posts.")

    def like_posts(self, user_data):
        token = self.tokens.get(user_data['username'])

        if token:
            num_likes = random.randint(1, self.config['max_likes_per_user'])
            for _ in range(num_likes):
                post_id = random.choice(
                    list(self.post_unique_identifiers.values()))
                url = f"{self.base_url}/api/posts/{post_id}/like_action/"
                headers = {'Authorization': f'JWT {token}'}
                response = requests.post(url=url, headers=headers)

                if response.status_code == 201:
                    logger.info(
                        f"User {user_data['username']} liked post with id {post_id}")
                elif response.status_code == 400:
                    logger.warning(
                        f"User {user_data['username']} already liked post with id {post_id}")
                else:
                    logger.warning(
                        f"User {user_data['username']} can't like post with id {post_id}")
        else:
            logger.warning(
                f"No token found for user {user_data['username']}. Unable to create posts.")


if __name__ == "__main__":
    bot = Bot("bot/config.json", "http://127.0.0.1:8000")
    bot.simulate_activity()
