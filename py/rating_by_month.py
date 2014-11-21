

import json
from datetime import datetime
from datetime import timedelta

DATA_FILE = '../json/review.json'
MIN_RATINGS = 500

import matplotlib.pyplot as plt
from util import *

def split_data():
    counts = {}
    biz_to_name = map_biz_id_to_name()
    with open(DATA_FILE, 'rb') as reader:
        for line in reader:
            try:
                review = json.loads(line)
            except ValueError, e:
                continue
            month = review['date'].split('-')[1]
            stars = review['stars']
            biz = review['business_id']
            if not counts.get(biz):
                counts[biz] = {'good': {}, 'bad': {}}
            if stars <= 3:
                if not counts[biz]['bad'].get(month):
                    counts[biz]['bad'][month] = 1
                else:
                    counts[biz]['bad'][month] += 1
            else:
                if not counts[biz]['good'].get(month):
                    counts[biz]['good'][month] = 1
                else:
                    counts[biz]['good'][month] += 1

    for biz, ratings in counts.iteritems():
        good = ratings['good']
        bad = ratings['bad']

        if sum(good.values()) + sum(bad.values()) < MIN_RATINGS:
            continue
        
        tuples = sorted(good.items(), key=lambda a: a[0])
        dates = [a[0] for a in tuples]
        counts = [a[1] for a in tuples]
        # smoothed = smooth_counts(pcounts)

        p, = plt.plot(dates, counts, label="Positive Reviews")
        
        tuples = sorted(bad.items(), key=lambda a: a[0])
        dates = [a[0] for a in tuples]
        counts = [a[1] for a in tuples]
        # smoothed = smooth_counts(ncounts)

        n, = plt.plot(dates, counts, label="Negative Reviews")
        plt.title(biz_to_name[biz] + " Review Counts By Month")
        plt.xlabel('Month Number')
        plt.ylabel('Number of Reviews')
        plt.legend(handles=[p, n])
        plt.savefig('../results/over_time/by_month/' + biz + '_month.png')
        plt.clf()

def smooth_counts(counts):
    count = counts[0]
    smoothed = []
    window = [count, count, count]
    for c in counts: 
        smoothed.append((sum(window) + c) / 4.0)
        window = window[1:]
        window.append(c)
    return smoothed



if __name__ == "__main__":
    split_data()
    