# -*- coding: utf-8 -*-
import json
import random

from app.utils import format_datetime, check_avatar, check_nickname
from app import db


def get_user_list(page, page_size=100):
    """获取用户列表"""
    user_col = db.auth_userinfo

    offset = page * page_size

    query_dict = {}
    if page == 0:
        query_dict['status'] = 1

    qs = user_col.find(query_dict).skip(offset).limit(page_size)

    result = []
    for inx, rec in enumerate(qs):
        userinfo = format_record(rec)
        userinfo['id'] = inx + 1

        result.append(userinfo)

    save_users = user_col.count_documents({'status': 1})
    total = user_col.count_documents(query_dict)
    total_page = (total + page_size - 1) // page_size

    return result, total_page, save_users


def save_users(user_uids: list):
    """添加用户"""
    user_col = db.auth_userinfo

    user_col.update_many(
        {'uid': {'$in': user_uids}},
        {'$set': {'status': 1}}
    )
    return True


def unsave_users(user_uids: list):
    """移除用户"""
    user_col = db.auth_userinfo

    user_col.update_many(
        {'uid': {'$in': user_uids}},
        {'$set': {'status': 0}}
    )
    return True


def get_saved_users_json(offset=0, limit=100):
    """获取保存的用户json"""
    user_col = db.auth_userinfo

    result = []
    for rec in user_col.find({}).skip(offset).limit(limit):
        result.append({
            'nickname': rec['nickname'],
            'city': rec['region']['city'],
            'avatar': rec['avatar'],
            'province': rec['region']['region']
        })

    return result


def auto_save():
    """自动过滤"""
    user_col = db.auth_userinfo

    invalid_ims = []

    i_uids = []
    loaded = 0
    for rec in user_col.find({'status': 0}).skip(73000 - 37500):
        nickname = rec['nickname']
        uid = rec['uid']
        avatar = rec.get('avatar_url', '')
        if check_nickname(nickname):
            if check_avatar(avatar):
                i_uids.append(uid)
                # print(uid, nickname, avatar)
            else:
                invalid_ims.append(avatar)

        loaded += 1
        if i_uids and len(i_uids) % 100 == 0:
            save_users(i_uids)
            i_uids = []

            print('Loaded %s =================================' % loaded)

    
    if i_uids:
       save_users(i_uids)

    with open('invalid_ims.json', 'w+') as fp:
        json.dump(invalid_ims, fp)

    return True



def format_record(rec: dict):
    region = rec['region']
    doc = {
        'id': 0,
        'chn': rec['chn'],
        'uid': rec['uid'],
        'openid': rec['openid'],
        'platform': '',
        'avatar': rec['avatar_url'],
        'nickname': rec['nickname'],
        'province': region['region'],
        'city': region['city'],
        'country': region['country'],
        'model': '',
        'version': '',
        'status': rec.get('status', 0),

        'create_time': format_datetime(rec['create_time']),
        'login_time': format_datetime(rec['modify_time']),
    }
    return doc

