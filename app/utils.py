# -*- coding: utf-8 -*-

import re
import pytz
from datetime import datetime


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
