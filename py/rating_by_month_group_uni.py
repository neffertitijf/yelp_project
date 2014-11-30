

import json
from datetime import datetime
from datetime import timedelta

DATA_FILE = '../json/review.json'
MIN_RATINGS = 500

import matplotlib.pyplot as plt
from util import *

def split_data():
    counts = {}
    biz_to_uni = load_biz_to_uni()
    with open(DATA_FILE, 'rb') as reader:
        for line in reader:
            try:
                review = json.loads(line)
            except ValueError, e:
                continue
            month = review['date'].split('-')[1]
            stars = review['stars']
            biz = review['business_id']
            unis = biz_to_uni[biz]
            for uni in unis:
                counts.setdefault(uni, {'good': {}, 'bad': {}})
                if stars <= 3:
                    if not counts[uni]['bad'].get(month):
                        counts[uni]['bad'][month] = 1
                    else:
                        counts[uni]['bad'][month] += 1
                else:
                    if not counts[uni]['good'].get(month):
                        counts[uni]['good'][month] = 1
                    else:
                        counts[uni]['good'][month] += 1

    for uni, ratings in counts.iteritems():
        good = ratings['good']
        bad = ratings['bad']
        
        tuples = sorted(good.items(), key=lambda a: a[0])
        dates = [a[0] for a in tuples]
        counts = [a[1] for a in tuples]

        p, = plt.plot(dates, counts, label="Positive Reviews")
        
        tuples = sorted(bad.items(), key=lambda a: a[0])
        dates = [a[0] for a in tuples]
        counts = [a[1] for a in tuples]

        n, = plt.plot(dates, counts, label="Negative Reviews")
        plt.title(uni + " Review Counts By Month")
        plt.xlabel('Month Number')
        plt.ylabel('Number of Reviews')
        plt.legend(handles=[p, n])
        plt.savefig('../results/over_time/by_month/' + uni + '_month.png')
        plt.clf()



if __name__ == "__main__":
    split_data()
    