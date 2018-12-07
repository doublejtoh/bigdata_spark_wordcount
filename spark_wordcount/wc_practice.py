# -*- coding: utf-8 -*-
import sys
import re
import os
from operator import add

from pyspark import SparkContext

# HDFS_PREFIX = "hdfs://localhost:9000/user/hadoop/"

def map_phase(x):
    x = re.sub('--', ' ', x)
    x = re.sub("'", '', x)
    return re.sub('[?!@#$\'",.;:()]', '', x).lower()

if __name__ == "__main__":
	if len(sys.argv) < 4:
	    print >> sys.stderr, "Usage: wordcount <master> <inputfile> <outputfile>"
	    exit(-1)
	sc = SparkContext(sys.argv[1], "python_wordcount_sorted in bigdataprogrammiing")
	lines = sc.textFile(sys.argv[2], 2) # input file parition 2개로 설정. 3개,4개로 설정해볼것.
	print("number of partitions: ", lines.getNumPartitions()) # print the number of partitions
	#print("lines: ", lines.collect())
		
	lines = lines.map(lambda x: map_phase(x))
	# print("lower cased collect: ", lines.collect())
	lines = lines.filter(lambda x: False if "tokyo" in x else True)#"tokyo" in x == True)
	# print("filtered collect: ", lines.collect())
	lines = lines.map(lambda x: (str(x), 1))
	lines = lines.reduceByKey(lambda x, y : x + y)
	# print("reducer output: ", lines.collect())
	lines = sorted(lines.collect())
	# print("sorted reducer ouptut: ", lines)
	outRDD = sc.parallelize(lines)
	outRDD.saveAsTextFile(sys.argv[3])
