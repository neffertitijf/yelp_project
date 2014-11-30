

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
            date = review['date']
            stars = review['stars']
            biz = review['business_id']
            unis = biz_to_uni[biz]
            for uni in unis:
                counts.setdefault(uni, {'good': {}, 'bad': {}})
                if stars <= 3:
                    if not counts[uni]['bad'].get(date):
                        counts[uni]['bad'][date] = 1
                    else:
                        counts[uni]['bad'][date] += 1
                else:
                    if not counts[uni]['good'].get(date):
                        counts[uni]['good'][date] = 1
                    else:
                        counts[uni]['good'][date] += 1

    # for uni, ratings in counts.iteritems():
    #     good = ratings['good']
    #     bad = ratings['bad']
        
    #     pds, pcounts = aggregate_counts(good.items())

    #     p, = plt.plot(pds, pcounts, label="Positive Reviews")
        
    #     nds, ncounts = aggregate_counts(bad.items())

    #     n, = plt.plot(nds, ncounts, label="Negative Reviews")
    #     plt.title(uni + " Cumilative Number of Reviews")
    #     plt.xlabel('Time')
    #     plt.ylabel('Number of Reviews')
    #     plt.legend(handles=[p, n])
    #     plt.savefig('../results/over_time/by_uni/' + uni + '.png')
    #     plt.clf()

def aggregate_counts(tuples):
    tuples = sorted(tuples, key=lambda a: a[0])
    ds = [datetime.strptime(k[0], '%Y-%m-%d') for k in tuples]
    neg_count = [k[1] for k in tuples]
    new_ds = []
    new_counts = []
    d = ds[0]
    rev = 0
    for nd, n in zip(ds, neg_count):
        if nd - d >= timedelta(days=31):
            new_counts.append(rev)
            new_ds.append(d)
            d = nd
        rev += n
    return new_ds, new_counts








if __name__ == "__main__":
    split_data()
    