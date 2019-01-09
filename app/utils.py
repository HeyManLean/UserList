# -*- coding: utf-8 -*-

import re
from datetime import datetime


def format_datetime(dt: datetime):
    return dt.strftime('%Y年%m月%d %H时%M分')


def clear_mobile_model(model):
    p1 = re.compile(r'\(.*\)')
    p2 = re.compile(r'<.*>')

    model = p1.sub('', model)
    model = p2.sub('', model)
    return model[:18]
