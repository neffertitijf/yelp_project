
from nltk.corpus import stopwords
from collections import Counter
import json
import csv

DATA_FILE = '../json/review.json'


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

def run():
    counts = {}
    uni_dicts = {}
    biz_to_uni_mp = load_biz_to_uni()
    stop = stopwords.words('english')
    with open(DATA_FILE, 'rb') as reader:        
        for line in reader:
            try:
                review = json.loads(line)
            except ValueError, e:
                continue
            unis = biz_to_uni_mp.get(review['business_id'])
            if not unis:
                continue
            for uni in unis:
                uni_dicts.setdefault(uni, Counter())
                counts.setdefault(uni, 0)
                counts[uni] += 1
            
            text = review['text']
            for word in text.lower().split():
                if word not in stop:
                    for uni in unis:
                        uni_dicts[uni][word] += 1

    with open('../results/uni_words.csv', 'wb') as f:
        csvwriter = csv.writer(f)
        for school, cnt in uni_dicts.iteritems():
            most_common = cnt.most_common(20)
            words = [school]
            perc = [school]
            for word, count in most_common:
                words.append(word)
                perc.append(count / float(counts[uni]))
            
            csvwriter.writerow(words)
            csvwriter.writerow(perc)

if __name__ == "__main__":
    run()