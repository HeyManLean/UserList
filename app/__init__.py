# -*- utf-8 -*-

from flask import Flask
from flask import render_template
from flask import redirect
from flask import request
from pymongo import MongoClient


client = MongoClient('mongodb://root:lewantest@172.16.1.201:27017/admin')
db = client['mini']
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


@app.route('/', methods=['GET'])
def index():
    return redirect('/1')


@app.route('/<int:page>', methods=['GET'])
def get_list(page: int):
    from app.model import get_user_list
    user_list, total_page, saved_users = get_user_list(page)
    return render_template(
        'index.html',
        user_list=user_list,
        total_page=total_page,
        current_page=page,
        saved_users=saved_users,
        count=len(user_list)
    )


@app.route('/api/users', methods=['POST', 'DELETE'])
def handle_users():
    data = request.json
    user_uids = data['uids']

    if request.method == 'POST':
        from app.model import save_users
        save_users(user_uids)
    else:
        from app.model import unsave_users
        unsave_users(user_uids)
    return ''
