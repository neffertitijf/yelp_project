
import json

DATA_FILE = 'yelp_academic_dataset.json'


def parse_data():
    with open(DATA_FILE, 'rb') as reader:
        user, biz, review = 0, 0, 0
        for line in reader:
            try:
                data = json.loads(line)
            except ValueError, e:
                continue
            obj_type = data.get('type')
            if obj_type == 'business':
                biz += 1
            elif obj_type == 'review':
                review += 1
            elif obj_type == 'user':
                user += 1
        print user, biz, review
























if __name__ == "__main__":
    parse_data()