import json

from flask import Blueprint, jsonify, request

from api_view.utils import user_request
from service.post_service import list_posts_for_user, create_post, list_posts_for_other, list_comments_on_post, \
    add_comment_on_post, add_like_to_post
from utils.logger import posts_logger

post_views = Blueprint('posts', __name__)


@post_views.route('/posts/list/my')
@user_request
def list_my_posts(user):
    print(user)
    r_data = []
    for post in list_posts_for_user(user.id):
        r_data.append(
            post.to_dict()
        )
    return jsonify(r_data), 200


@post_views.route('/posts/list/other')
@user_request
def list_other_posts(user):
    r_data = []
    for post in list_posts_for_other(user.id):
        r_data.append(
            post.to_dict()
        )
    return jsonify(r_data), 200


@post_views.route('/posts/comments/<post_id>/')
@user_request
def get_comments_for_post(user, post_id):
    comments = list_comments_on_post(post_id)
    return jsonify([comment.to_dict() for comment in comments])


@post_views.route('/posts/comments/<post_id>/add/', methods=['POST'])
@user_request
def add_comment_on_post_view(user, post_id):
    try:
        data = request.json
        add_comment_on_post(post_id, user.id, data.get('message'))
        return 'Success', 200
    except Exception as ex:
        return 'Bad request', 400


@post_views.route('/posts/<post_id>/like/add/', methods=['POST'])
@user_request
def add_like_to_post_view(user, post_id):
    try:
        add_like_to_post(post_id, user.id)
        return 'Success', 200
    except Exception as ex:
        posts_logger.error(f'Request to like post {post_id} by user {user.id} failed with exception: {str(ex)}')
        posts_logger.exception(ex)
        return 'Bad request', 400


@post_views.route('/posts/<post_id>/like/')
@user_request
def get_likes_on_post(user, post_id):
    likes = get_likes_on_post(post_id)
    return jsonify([comment.to_dict() for comment in likes])


@post_views.route('/posts/add', methods=['POST'])
@user_request
def add_post(user):
    req_data = json.loads(request.data)
    title = req_data.get('title')
    message = req_data.get('message')
    if not title and not message:
        return jsonify(dict(message='At least title or message is required')), 400
    if not title:
        title = message.split(' ')[0]
    if not message:
        message = title
    post = create_post(title, message, user)
    return jsonify(dict(id=post.id)), 200
