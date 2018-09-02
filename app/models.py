import datetime
import jwt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from app.settings import Config
import uuid

db = SQLAlchemy()
migrate = Migrate()


class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    uuid = db.Column(db.String(length=32), default=lambda: uuid.uuid4().hex, unique=True, index=True)
    phonenum = db.Column(db.String(length=100))
    password = db.Column(db.String(length=100))
    last_login_at = db.Column(db.DateTime())
    token = db.Column(db.String(200), default="")
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)

    def __init__(self, phonenum, password):
        self.phonenum = phonenum
        self.set_password(password)
        self.gen_login_time()
        self.gen_token()

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, value):
        return check_password_hash(self.password, value)

    def gen_login_time(self):
        last_login = datetime.datetime.utcnow()
        self.last_login_at = last_login

    def gen_token(self):
        # 生成JWT
        payload = {
            'exp': self.last_login_at + datetime.timedelta(days=10, seconds=0),
            'iat': self.last_login_at,
            'sub': self.phonenum
        }
        token = jwt.encode(
            payload,
            Config.SECRET_KEY,
            algorithm='HS256'
        )
        token = token.decode('utf-8')
        self.token = token

    def __repr__(self):
        return '<User %r>' % self.phonenum


class Post(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    title = db.Column(db.String(length=30))
    content = db.Column(db.String(length=30))
    n_likes = db.Column(db.Integer(),default=0)
    n_comments = db.Column(db.Integer(),default=0)
    post_type = db.Column(db.Integer())
    created_at=db.Column(db.DateTime())
    def __init__(self, title, content, n_likes, n_comments, post_type):
        self.title = title
        self.content = content
        self.n_likes = n_likes
        self.n_comments = n_comments
        self.post_type = post_type
        self.get_created_at()

    def get_created_at(self):
        created_at = datetime.datetime.utcnow()
        self.created_at = created_at

    def __repr__(self):
        return '<User %r>' % self.title

