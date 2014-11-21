
import json

def map_biz_id_to_name():
    mp = {}
    with open('../json/biz.json', 'rb') as reader:
        for line in reader:
            try:
                biz = json.loads(line)
            except ValueError, e:
                continue
            mp[biz['business_id']] = biz['name']
    return mp


def load_biz_to_uni():
    mp = {}
    with open('../json/biz.json', 'rb') as reader:
        for line in reader:
            try:
                biz = json.loads(line)
            except ValueError, e:
                continue
            mp[biz['business_id']] = biz['schools']
    return mp