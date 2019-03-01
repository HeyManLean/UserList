# -*- coding: utf-8 -*-

import re
import pytz
from datetime import datetime
from io import BytesIO

import requests
from PIL import Image
import numpy as np


INVALID_IM = Image.open('132.png').convert('L')
INVALID_ARR = np.array(INVALID_IM)


def utc_to_local_datetime(dt: datetime, local_timezone="Asia/Shanghai"):
    """把utc datetime 转换为本地市区的时间"""
    return dt.replace(tzinfo=pytz.utc).astimezone(pytz.timezone(local_timezone))


def format_datetime(dt: datetime):
    dt = utc_to_local_datetime(dt)
    return dt.strftime('%m-%d %H:%M')


def clear_mobile_model(model):
    p1 = re.compile(r'\(.*\)')
    p2 = re.compile(r'<.*>')

    model = p1.sub('', model)
    model = p2.sub('', model)
    return model[:12]


INVALID_KEYWORDS = [
    '公司', '家', '店', '铺', '编号', '房', '室', '投资', '饰', '外卖',
    '系统', '车', '手机', '化妆', '贷', '保险', '经理', '阁', '公寓',
    '柜', '橱', '信用', '卡', '彩票', '商', '院', '校', '区',
    '厂', '维修', '配件', '行业', '二手', '销售', 'KTV', '火锅',
    '桌子', '中国', '聘', '城', '市', '省', '国', '业', '工程', '金融', '楼', '售',
    '客', '休闲', '税', '销', '科技', '信息', '号', '美容', '粉红', '名',
    '厨', '财', '酒', '买', '卖', '产', '队', '代', '社', '党', '枪', '创',
    '招', '空间', '物流', '品', '电', '师', '钢', '管', '警', '团', '牌', '赌', '毒',
    '机', '塑', '馆', '金', '银', '肾', '洗', '服务', '府', '门', '身', '购', '装',
    '批', 'A', '健康', '输入', 'QQ', '员', '会', '衣', '男', '女', '医', '钱', '币', '课',
    '妹', '哥', '姐', '弟', '爸', '妈', '广告', '快递', '对方', '皮肤', '祛', '输入',
    "微整", "整型", "保健", "按摩", "奶", "摩托", "平安", "胸", '主席', '学生', '锅', '婴',
    '旅', '推广', '坊', '仿', '优惠', '淘', '啪', '寂寞', '老板', '王者', '空调', '合伙',
    '饭', '艳', '睫', '投注', '彩印', '眼镜', '屎', '美甲', '贸', '航空', '肤', '养', '宠物',
    '网', '汽', '礼', '材', '咖啡', '珠宝', 'YY', '丫丫', '烟', '贱', '修', '¥', '教', '育',
    '涂', '造型', '支付', '滚', '蛋'
]


def check_nickname(nickname):
    """检查昵称是否合法"""
    if not nickname:
        return False
    if len(nickname) > 10:
        return False
    if len(set(nickname)) == 1:
        return False
    # ret = re.search(r"1[35678]\d{9}", nickname)
    # if ret:
    #     return False
    ret = re.search(r'\d{6}', nickname)
    if ret:
        return False
    for key in INVALID_KEYWORDS:
        if key in nickname:
            return False
    return True


def check_avatar(image_url):
    if not image_url or not image_url.startswith('http'):
        return False
    try:
        res = requests.get(image_url, timeout=10)
        bio = BytesIO(res.content)
        im_arr = np.array(Image.open(bio).convert('L'))
    except Exception:
        return False

    result = (im_arr[0] == INVALID_ARR[0])
    if isinstance(result, np.ndarray):
        result = result.all()
    if result:
        print(image_url, 'IS INVALID')
        return False
    else:
        return True