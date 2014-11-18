

import json
from datetime import datetime
from datetime import timedelta

DATA_FILE = 'review.json'
MIN_RATINGS = 500

import matplotlib.pyplot as plt


def split_data():
    counts = {}
    with open(DATA_FILE, 'rb') as reader:
        for line in reader:
            try:
                review = json.loads(line)
            except ValueError, e:
                continue
            date = review['date']
            stars = review['stars']
            biz = review['business_id']
            if not counts.get(biz):
                counts[biz] = {'good': {}, 'bad': {}}
            if stars <= 3:
                if not counts[biz]['bad'].get(date):
                    counts[biz]['bad'][date] = 1
                else:
                    counts[biz]['bad'][date] += 1
            else:
                if not counts[biz]['good'].get(date):
                    counts[biz]['good'][date] = 1
                else:
                    counts[biz]['good'][date] += 1

    for biz, ratings in counts.iteritems():
        good = ratings['good']
        bad = ratings['bad']

        if sum(good.values()) + sum(bad.values()) < MIN_RATINGS:
            continue
        print biz
        
        pds, pcounts = aggregate_counts(good.items())
        smoothed = smooth_counts(pcounts)

        plt.plot(pds, smoothed)
        
        nds, ncounts = aggregate_counts(bad.items())
        smoothed = smooth_counts(ncounts)

        plt.plot(nds, smoothed)
        plt.show()
        break

def smooth_counts(counts):
    count = counts[0]
    smoothed = []
    window = [count, count, count]
    for c in counts: 
        smoothed.append((sum(window) + c) / 4.0)
        window = window[1:]
        window.append(c)
    return smoothed

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
            rev = n
            new_ds.append(d)
            d = nd
        else:
            rev += n
    return new_ds, new_counts



















if __name__ == "__main__":
    split_data()
    