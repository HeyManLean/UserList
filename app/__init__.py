# -*- utf-8 -*-

from flask import Flask
from flask import render_template
from flask import redirect
from flask import request

from app.model import get_user_list


app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return redirect('/1')


@app.route('/<int:page>', methods=['GET'])
def get_list(page: int):
    col_names = [
        '次序', '图像', '昵称', '游戏代号', '系统', 
        '省份', '城市', '性别', '注册时间', '最近登录时间', '是否录入'
    ]
    user_list, total_page = get_user_list(page)
    return render_template(
        'index.html', 
        col_names=col_names, 
        user_list=user_list,
        total_page=total_page
    )


@app.route('/api/users', methods=['POST', 'DELETE'])
def handle_users():
    data = request.json
    user_uids = data['uids']

    if request.method == 'POST':
        print(user_uids, 'post')
    else:
        print(user_uids, 'delete')
    return ''
