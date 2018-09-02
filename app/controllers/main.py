import datetime

from flask import Blueprint, request, jsonify
from app.models import User, db, Post
from app.utils.auth_utils import login_required
from sqlalchemy import text
main = Blueprint('main', __name__, url_prefix="/api/1.0/")

@main.route('/')
def home():
    return jsonify('home')


@main.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(phonenum=data['phonenum']).one()
    user.last_login_at = datetime.datetime.now()
    db.session.commit()
    if user.check_password(data['password']):
        return jsonify(status=True, message='Logged in successfully.', token=user.token)
    else:
        return jsonify(status=False, message='Invalid username or password.')


@main.route("/logout")
def logout():
    return jsonify(status=True, message='You have been logged out.')


@main.route("/user_info", methods=['GET'])
@login_required
def user_info():
    return jsonify(status=True, data={
        "user_phone": request.user.phonenum,
        "last_login_at": str(request.user.last_login_at)
    })

@main.route("/get_posts",method=['GET'])
def getpost():
    for user in Post.query.filter_by(post_type = 0).all():
        print(user)


@main.route("/send_post",methods=['POST'])
def sendpost():
    data = request.get_json()
    p =Post(data['title'],data['content'],data['n_likes'],data['n_comments'],data['post_type'])
    db.session.add(p)
    db.session.commit()
    return jsonify('success')



