import datetime

from flask import Blueprint, request, jsonify
from app.models import User, db, Post
from app.utils.auth_utils import login_required
from sqlalchemy import text
main = Blueprint('main', __name__, url_prefix="/api/1.0/")


number=0
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

@main.route("/get_post",methods=['GET'])
def getpost():
    try:
        a=Post.query.filter_by(post_type='0').all()
    except Exception as e:
        fresponse=jsonify({
            'status':False,
             'message':'查询失败'
        })
        return fresponse
    else:
        b = Post.query.filter_by(post_type='0').all()
        for m in b:
            sresponse=jsonify({
                'status':True,
                'data':[{
                    'title': m.title, 'content': m.content, 'n_likes': m.n_likes,
                    'n_comments': m.n_comments, 'post_type': m.post_type, 'created_at': m.created_at
                }]
            })
            print(sresponse)
        return jsonify(0)



@main.route("/send_post",methods=['POST'])
def sendpost():
    try:
        data = request.get_json()
        p =Post(data['title'],data['content'],data['n_likes'],data['n_comments'],data['post_type'])
        db.session.add(p)
        db.session.commit()

    except Exception as e:
        fresponse = jsonify({
            'status': False,
            'message': '插入失败，请检查您的title、content、n_likes、n_comments、post_type信息是否完整并按照定义输入'
        })
        return fresponse
    else:
        global number
        number+=1
        sresponse = jsonify({
            'status': True,
            'message': '插入成功'
        })
    return sresponse



