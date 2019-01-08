# -*- coding: utf-8 -*-

import random


def get_user_list(page, page_size=10):
    offset = (page - 1) * page_size
    limit = page_size

    result = []

    records = TEST_RECORD_LIST[offset: offset + limit]
    total_page = (len(TEST_RECORD_LIST) + page_size - 1) // page_size

    for rec_index, rec in enumerate(records):
        user_info = {
            'id': rec_index + 1,
            'uid': rec['uid'],
            'chn': rec['chn'],
            'os': rec['base']['os'],
            'avatar': rec['wx_userinfo']['avatarUrl'],
            'nickname': rec['wx_userinfo']['nickName'],
            'province': rec['wx_userinfo']['province'],
            'city': rec['wx_userinfo']['city'],
            'gender': '男' if rec['wx_userinfo']['gender'] else '女',
            'create_time': rec['registered_time'],
            'login_time': rec['modified_time'],
            'status': random.randint(0, 1)
        }
        result.append(user_info)
    return result, total_page


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