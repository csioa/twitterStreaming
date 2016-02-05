from pyspark import SparkContext, SparkConf

sc = SparkContext()

# load txt file from directory. absolute path might need to be changed
moby_dickRDD = sc.textFile("/home/babis/twitterStreaming/Spark_tutorial/moby_dick.txt")

# flatMap to split every line into words
# filter out the words with length less than 7
# map every word to lowercase and match every it with number 1
# reduceByKey to group the tuples with the same key (word) together
mapred_mobyRDD = (moby_dickRDD.flatMap(lambda line: line.split(" "))
                              .filter(lambda word: len(word) >= 7)
                              .map(lambda word: (word.lower(), 1))
                              .reduceByKey(lambda a,b: a + b))

# switching from (word,count) to (count,word) to sort by count
mapred_mobyRDD = mapred_mobyRDD.map(lambda (x, y): (y,x))

# sort the tuples by the number of occurences - False is for ascending order
sorted_mobyRDD = mapred_mobyRDD.sortByKey(False)

# keep the 50 most popular words
top50 = sorted_mobyRDD.take(50)

print top50
