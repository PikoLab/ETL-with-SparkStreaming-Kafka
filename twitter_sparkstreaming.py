from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

from textblob import TextBlob
import preprocessor as p 


if __name__=="__main__":

	#<Step1> Create StreamingContext
	spark=SparkSession \
			.builder\
			.getOrCreate()

	sc=spark.sparkContext
	ssc=StreamingContext(sc,10)

	#<Step2> Connect to the data source
	raw_stream=KafkaUtils.createStream(ssc,"zookeeper:2181", "consumer-group",{"twitter_stream":1})\
						.window(300,20)

	#<Step3> Analysis with transformations and actions
	def output_rdd(rdd):
		df=spark.createDataFrame(rdd,"user string, score float")
		df.write.option("driver","com.mysql.jdbc.Driver") \
				.jdbc("jdbc:mysql://localhost:3306",
						"twitter.realtime_sentiment_analysis",
						mode="overwrite",
						properties={"user":"root","password":"root"})


	raw_stream.mapValues(lambda message: (TextBlob(p.clean(message)).sentiment.polarity,1)) \
			.reduceByKey(lambda x,y: (x[0]+y[0],x[1]+y[1])) \
			.mapValues(lambda x:x[0]/x[1]) \
			.foreachRDD(output_rdd)

	#<Step4> Start and computation
	ssc.start()
	ssc.awaitTermination()