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
        print(rec_uid)
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


def get_saved_users_json(limit=None):
    mini_collection = db2.g10_fake_lucky_user
    if limit:
        records = mini_collection.find({}).limit(limit)
    else:
        records = mini_collection.find({})
    result = []
    for rec in records:
        # rec.pop("_id")
        # result.append(rec)

        result.append({
            'nickname': rec['nickname'],
            'city': rec['region']['city'],
            'avatar': rec['avatar']
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
    print(len(uids))
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


TEST_RECORD_LIST = [{ 
    "_id" : "5bf90f595ece0d1dde9b7e59", 
    "uid" : "323002", 
    "ip" : "61.144.146.248", 
    "session_key" : "vGyEx+TcjWF00cG2C4z0KA==", 
    "last_auth_time" : "2018-12-08T07:31:13.964+0000", 
    "registered_ip" : "61.144.144.210", 
    "ver" : "1.2.1", 
    "registered_channel_class" : "", 
    "chn" : "g10-1", 
    "platform" : "devtools", 
    "gid" : "18771545", 
    "registered_time" : "2018-11-24T08:44:09.563+0000", 
    "last_userinfo_time" : "2018-12-08T07:31:17.596+0000", 
    "openid" : "o3BD15Y4AGGpU8S3QzhOvEiPuTpA", 
    "registered_channel_entry" : "", 
    "registered_platform" : "devtools", 
    "modified_time" : "2018-12-08T07:31:17.596+0000", 
    "registered_ver" : "1.0.0", 
    "base" : {
        "wx_sdk" : "2.4.1", 
        "ip" : "61.144.146.248", 
        "window_width" : "414", 
        "platform" : "devtools", 
        "ver" : "1.2.1", 
        "network" : "", 
        "wx_app" : "6.6.3", 
        "window_height" : "736", 
        "chn" : "g10-1", 
        "channel_class" : "", 
        "screen_width" : "414", 
        "pixel_ratio" : "3", 
        "brand" : "devtools", 
        "font_size_setting" : "16", 
        "language" : "zh", 
        "status_bar_height" : "20", 
        "user_agent" : "Mozilla/5.0 (iPhone; CPU iPhone OS 10_2 like Mac OS X) AppleWebKit/602.3.12 (KHTML, like Gecko) Mobile/14C92 Safari/601.1 wechatdevtools/1.02.1811290 MicroMessenger/6.5.7 Language/zh_CN webview/20000 gameservice port/50559 token/a58e234bbdca9d42ab754f89e84098f1", 
        "debug" : "0", 
        "model" : "iPhone 7 Plus", 
        "os" : "iOS 10.0.1", 
        "channel_entry" : "", 
        "screen_height" : "736"
    }, 
    "registered_chn" : "g10-1", 
    "wx_userinfo" : {
        "province" : "Guangdong", 
        "openId" : "o3BD15Y4AGGpU8S3QzhOvEiPuTpA", 
        "language" : "zh_CN", 
        "city" : "Shantou", 
        "gender" : 1, 
        "avatarUrl" : "https://wx.qlogo.cn/mmopen/vi_32/siagDfnvFAspZIIhS215zGuYambQMephfIssBf1rVe71k0NWuecRvcw27avdQzDC0hbLGNIwSlia74Q0F0MfWkEw/132", 
        "watermark" : {
            "timestamp" : 1544254277, 
            "appid" : "wxf730db9d0a336f43"
        }, 
        "country" : "China", 
        "nickName" : "李康"
    }, 
    "unionid" : "", 
    "region" : {
        "ip" : "61.144.144.210", 
        "region" : "广州", 
        "isp" : "电信", 
        "city" : "广州", 
        "country" : "中国"
    }, 
    "appid" : "wxf730db9d0a336f43", 
    "channel_class" : "", 
    "channel_entry" : ""
} for _ in range(97)]