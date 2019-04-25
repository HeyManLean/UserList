# -*- utf-8 -*-

from flask import Flask
from flask import render_template
from flask import redirect
from flask import request
from flask import jsonify
from pymongo import MongoClient
from mongoengine import register_connection

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


MONGO_DBS = {
    'db201': ('mongodb://lwtest:lewantest@172.16.1.202:27017/admin', 'mini'),
    'db202': ('mongodb://lwtest:lewantest@172.16.1.202:27017/admin', 'mini_api')
}

mongo_dbs = {}


for key, value in MONGO_DBS.items():
    db_uri = value[0]
    db_name = value[1]
    client = MongoClient(db_uri)
    mongo_dbs[key] = client[db_name]

    alias = key
    # mongoengine支持程序同时连接多个数据库，这些数据库可以位于一个或多个mongo之中，通过alias名称区分不同的连接
    register_connection(db=db_name, alias=alias, host=db_uri)

db = mongo_dbs['db201']
db2 = mongo_dbs['db202']


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


@app.route('/api/json', methods=['GET'])
def get_saved_json():
    from app.model import get_saved_users_json
    limit = request.args.get('limit')
    if limit:
        data = get_saved_users_json(int(limit))
    else:
        data = get_saved_users_json()
    return jsonify(data)


@app.route('/api/auto_save', methods=['GET'])
def get_auto_save():
    from app.model import auto_save
    auto_save()
    return ''


@app.route('/api/auto_save2', methods=['GET'])
def get_auto_save2():
    from app.model import auto_save2
    auto_save2()
    return ''
