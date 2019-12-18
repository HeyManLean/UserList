#!/usr/bin/env python3
import re
import json


M_P = re.compile(r'^([0-9a-zA-Z\-]+):?')

data_list = []


with open('mobile.txt', 'r') as fp:
    for l in fp:
        res = M_P.match(l)
        if not res:
            continue

        data_list.append(res.group(1))

with open('mobile.json', 'w+') as fp:
    json.dump(data_list, fp)

