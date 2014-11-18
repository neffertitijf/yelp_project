
from nltk.corpus import stopwords
from collections import Counter
import json
import csv

DATA_FILE = '../json/review.json'


def run():
    counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    stop = stopwords.words('english')
    star_dicts = {1: Counter(), 2: Counter(), 3: Counter(), 4: Counter(), 5: Counter()}
    with open(DATA_FILE, 'rb') as reader:
        user, biz, review = 0, 0, 0
        
        for line in reader:
            try:
                review = json.loads(line)
            except ValueError, e:
                continue
            stars = int(review['stars'])
            counts[stars] += 1
            text = review['text']
            for word in text.lower().split():
                if word not in stop:
                    star_dicts[stars][word] += 1

    with open('../results/star_words.csv', 'wb') as f:
        csvwriter = csv.writer(f)
        for star, cnt in star_dicts.iteritems():
            most_common = cnt.most_common(20)
            words = [star]
            perc = [star]
            for word, count in most_common:
                words.append(word)
                perc.append(count / float(counts[star]))
            
            csvwriter.writerow(words)
            csvwriter.writerow(perc)
            

if __name__ == "__main__":
    run()