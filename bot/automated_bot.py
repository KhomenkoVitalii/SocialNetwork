import json
import random
import requests
from utils import generate_user_data, generate_user_post


class Bot:
    """
    Object of this bot demonstrate functionalities of the system according to defined rules. This bot
    read rules from a config file
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
            print('\n\n\n')
            user_data = generate_user_data()
            post_data = generate_user_post()
            self.signup_user(user_data)
            self.create_posts(user_data, post_data)
            self.like_posts(user_data)

    def signup_user(self, user_data):
        url = f"{self.base_url}/api/v1/auth/users/"
        response = requests.post(url, json=user_data)

        if response.status_code == 201:
            print(f"User {user_data['username']} signed up successfully.")
            self.user_unique_identifiers[user_data['username']] = response.json()[
                'id']
            print(f"User {user_data['username']} id stored successfully.")
            self.sign_in_user(user_data)
        else:
            print(f"Failed to sign up user {user_data['username']}.")

    def sign_in_user(self, user_data):
        url = f"{self.base_url}/api/v1/auth/jwt/create/"
        response = requests.post(url, data={'email': user_data.get(
            'email'), 'password': user_data.get('password')})

        if response.status_code == 200:
            self.tokens[user_data['username']] = response.json()['access']
            print(f"Stored {user_data.get('username')}'s token successfully!")
        else:
            print(f"Failed to sign in {user_data['username']}!")
            print(f"Got {response.status_code} status code")

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
                    print(
                        f"User {user_data['username']} created post successfully.")
                else:
                    print(
                        f"Failed to create post by user {user_data['username']}.")
                    print(response.json())
                    print(response.request.headers)
        else:
            print(
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
                    print(
                        f"User {user_data['username']} liked post with id {post_id}")
                elif response.status_code == 400:
                    print(
                        f"User {user_data['username']} already liked post with id {post_id}")
                else:
                    print(
                        f"User {user_data['username']} can't like post with id {post_id}")
        else:
            print(
                f"No token found for user {user_data['username']}. Unable to create posts.")


if __name__ == "__main__":
    bot = Bot("bot/config.json", "http://127.0.0.1:8000")
    bot.simulate_activity()
