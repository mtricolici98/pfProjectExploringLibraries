import json
import sys
from dataclasses import dataclass
from functools import wraps

import requests

from utils.logger import logger

API_URL = 'http://127.0.0.1:8080'


def validate_response(func):
    """
    Decorates functions that return a response
    and returns the JSON data if the response is valid
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)
        if response.status_code == 200:
            return response.json()
        is_json = response.headers.get('Content-Type') == 'application/json'
        response_info = response.json() if is_json else response.text
        raise Exception(
            f'Request failed with code {response.status_code},'
            f' data: {response_info}'
        )

    return wrapper


@dataclass
class Post:
    id: int
    message: str
    title: str

    def __repr__(self):
        return f'Post [{self.id}]\n {self.title} \n {self.message} \n\n'

    def __str__(self):
        return repr(self)


@dataclass
class Comment:
    id: int
    message: str


class PostApplicationClient:

    def __init__(self, username, password):
        self.token = self.login(username, password)

    @staticmethod
    def login(username, password):
        login_response = requests.post(
            f'{API_URL}/user/login',
            data=json.dumps(dict(
                login=username,
                password=password
            ))
        )
        if login_response.status_code == 200:
            login_data = login_response.json()
            return login_data.get('token')
        else:
            print('Could not authenitcate')
            sys.exit()

    @validate_response
    def _do_post_request(self, url, data, params=None):
        return requests.post(
            f'{API_URL}{url}',
            headers={
                'Auth-Token': self.token
            },
            data=json.dumps(data) if not type(data) == str else data,
            params=params
        )

    @validate_response
    def _do_get_request(self, url, params=None):
        return requests.get(
            f'{API_URL}{url}',
            headers={
                'Auth-Token': self.token
            },
            params=params
        )

    def get_my_posts(self):
        logger.info('Getting post lists for current user')
        data = self._do_get_request('/posts/list/my')
        converted_data = [Post(**info) for info in data]
        return converted_data

    def get_post_comments(self, post_id):
        logger.info('Getting post lists for current user')
        data = self._do_get_request(f'/posts/comments/{post_id}/')
        converted_data = [Comment(**info) for info in data]
        return converted_data

    def make_new_post(self, title, message):
        return self._do_post_request('/posts/add', data={
            'title': title,
            'message': message,
        })


client = PostApplicationClient('mt', 'pass')
logger.info(f'Logging in with user mt and password pass')
for post in client.get_my_posts():
    print(post)
print(client.get_post_comments(1))
client.make_new_post(
    input('Title'),
    input('Message')
)
print(client.get_my_posts())
