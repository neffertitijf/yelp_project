import json
import sys
from mrjob.job import MRJob

class YelpBiz(MRJob):
	def mapper(self,_,line):
		data=json.loads(line)
		if data["type"]=="business":
			for i in data["categories"]:
				yield i,1
	
	def reducer(self,key,values):
		yield key, sum(values)

if __name__=='__main__':
	YelpBiz.run()
