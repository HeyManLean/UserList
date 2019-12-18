# -*- coding: utf-8 -*-

import random
import json
from datetime import datetime

import pymongo

from app import db, db2
from app.utils import format_datetime
from app.utils import clear_mobile_model
from app.utils import check_nickname
from app.utils import check_avatar


def get_user_list(page, page_size=200):
    result = []

    uid_set = get_save_uid_set()
    if page != 0:
        offset = (page - 1) * page_size
        records, total = get_user_records(offset, page_size)
        total_page = (total + page_size - 1) // page_size
    else:
        records = get_saved_records(uid_set)
        total_page = 1

    for rec_index, rec in enumerate(records):
        rec_uid = rec['uid']
        user_info = {
            'id': rec_index + 1,
            'uid': rec['uid'],
            'chn': rec['chn'],
            'platform': rec['registered_platform'],
            'avatar': rec['wx_userinfo']['avatarUrl'],
            'nickname': rec['wx_userinfo']['nickName'].strip()[:16],
            'province': rec['region'].get('region'),
            'city': rec['region'].get('city'),
            'gender': '男' if rec['wx_userinfo']['gender'] == 1 else '女',
            'create_time': format_datetime(rec['registered_time']),
            'login_time': format_datetime(rec['last_auth_time']),
            'status': 1 if rec_uid in uid_set else 0,
            'model': clear_mobile_model(rec['base']['model']),
            'version': rec['ver']
        }
        result.append(user_info)
    return result, total_page, len(uid_set)


def get_saved_records(uid_set):
    records = []
    mini_user_collection = db.u_userinfo
    for uid in uid_set:
        query_dict = {
            "uid": uid
        }
        rec = mini_user_collection.find_one(query_dict)
        if rec is not None:
            records.append(rec)
    return records

def get_user_records(offset, limit):
    mini_user_collection = db.u_userinfo
    query_dict = {
        "wx_userinfo.openId": {"$exists": 1},
        "wx_userinfo.avatarUrl": {"$ne": ''},
        "region.city": {"$nin": ["北京", "上海", "广州", "深圳", "境外", "厦门", "成都", ""]},
        "region.region": {"$ne": "广东"}
    }
    records = mini_user_collection.find(query_dict).skip(offset).limit(limit)
        
    total = mini_user_collection.find(query_dict).count()

    return records, total


def get_save_uid_set():
    mini_collection = db2.g10_fake_lucky_user
    parse_dict = {
        "uid": True
    }
    uid_set = set()

    records = mini_collection.find({}, parse_dict)
    for rec in records:
        uid_set.add(rec['uid'])
    return uid_set


def save_users(uids):
    uids = list(set(uids))
    mini_collection = db2.g10_fake_lucky_user
    mini_user_collection = db.u_userinfo

    for uid in uids:
        query_dict = {
            "uid": uid,
            "wx_userinfo.openId": {"$exists": 1},
            "region.city": {"$nin": ["北京", "上海", "广州", "深圳", "境外", "厦门", "成都"]}
        }
        user_record = mini_user_collection.find_one(query_dict)
        if not user_record:
            continue

        user_region = user_record['region']
        query_dict = {"uid": uid}
        doc = {
            "uid": uid,
            
            "region" : user_region,

            # 微信数据
            "ip": user_record["ip"],
            "city" : user_record['wx_userinfo']['city'], 
            'province': user_record['wx_userinfo']['province'],
            "country" : user_record['wx_userinfo']['country'],
            "openid": user_record['wx_userinfo']['openId'],
            'chn': user_record['chn'],

            'platform': user_record['registered_platform'],
            'avatar': user_record['wx_userinfo']['avatarUrl'],
            'nickname': user_record['wx_userinfo']['nickName'],
            'gender': user_record['wx_userinfo']['gender'],
            'create_time': user_record['registered_time'],
            'login_time': user_record['last_auth_time'],
            'model': user_record['base']['model'],
            'version': user_record['ver']
        }
        mini_collection.replace_one(query_dict, doc, upsert=True)
    return True


def unsave_users(uids):
    uids = list(set(uids))
    mini_collection = db2.g10_fake_lucky_user

    for uid in uids:
        query_dict = {
            "uid": uid
        }
        mini_collection.remove(query_dict)
    return True


def get_saved_users_json(offset=0, limit=None):
    mini_collection = db2.g10_fake_lucky_user
    if limit:
        records = mini_collection.find({}).skip(offset).limit(limit)
    else:
        records = mini_collection.find({}).skip(offset)
    result = []
    for rec in records:
        # rec.pop("_id")
        # result.append(rec)

        result.append({
            'nickname': rec['nickname'],
            'city': rec['region']['city'],
            'avatar': rec['avatar'],
            'province': rec['region']['region']
        })
    return result


def auto_save():
    uids = []
    invalid_ims = []
    for i in range(1500, 2000):
        i_uids = []
        users, _, _ = get_user_list(i, 100)
        for user in users:
            nickname = user.get('nickname')
            uid = user.get('uid')
            avatar = user.get('avatar')

            if check_nickname(nickname):
                if check_avatar(avatar):
                    uids.append(uid)
                    i_uids.append(uid)
                    print(uid, nickname, avatar)
                else:
                    invalid_ims.append(avatar)
        save_users(i_uids)
    with open('invalid_ims.json', 'w+') as fp:
        json.dump(invalid_ims, fp)


def auto_save2():
    uids = []
    users = get_saved_users_json()
    for user in users:
        nickname = user.get('nickname')
        uid = user.get('uid')

        if check_nickname(nickname):
            uids.append(uid)
            print(uid, nickname)
    save_users2(uids)


def save_users2(uids):
    uids = list(set(uids))
    mini_collection = db2.g11_fake_lucky_user
    mini_user_collection = db.u_userinfo

    for uid in uids:
        query_dict = {
            "uid": uid,
            "wx_userinfo.openId": {"$exists": 1},
            "region.city": {"$nin": ["北京", "上海", "广州", "深圳", "境外", "厦门", "成都"]}
        }
        user_record = mini_user_collection.find_one(query_dict)
        if not user_record:
            continue

        user_region = user_record['region']
        query_dict = {"uid": uid}
        doc = {
            "uid": uid,
            
            "region" : user_region,

            # 微信数据
            "ip": user_record["ip"],
            "city" : user_record['wx_userinfo']['city'], 
            'province': user_record['wx_userinfo']['province'],
            "country" : user_record['wx_userinfo']['country'],
            "openid": user_record['wx_userinfo']['openId'],
            'chn': user_record['chn'],

            'platform': user_record['registered_platform'],
            'avatar': user_record['wx_userinfo']['avatarUrl'],
            'nickname': user_record['wx_userinfo']['nickName'],
            'gender': user_record['wx_userinfo']['gender'],
            'create_time': user_record['registered_time'],
            'login_time': user_record['last_auth_time'],
            'model': user_record['base']['model'],
            'version': user_record['ver']
        }
        mini_collection.replace_one(query_dict, doc, upsert=True)
    return True
