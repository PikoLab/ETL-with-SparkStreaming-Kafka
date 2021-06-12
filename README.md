# ETL with SparkStreaming and Kafka

### 1. Purpose: 
* Build Real-time Sentiment Engine
* Build Streaming Data Pipeline by integrating `Twitter Streaming API` with `Kafka` and `Spark Streaming`
* Using NLP libraries `TextBlob` and understanding the sentiment that people have towards the chosen keywords at the moment

### 2. Apache Kafka Quick Start

STEP1: Launch Zookeeper
```shell
$ cd ~/kafka_2.12-0.10.2.1/
$ bin/zookeeper-server-start.sh config/zookeeper.properties
```
STEP2: Launch Kafka Broker
```shell
$ bin/kafka-server-start.sh config/server-0.properties
$ bin/kafka-server-start.sh config/server-1.properties
$ bin/kafka-server-start.sh config/server-2.properties
```
STEP3: Create Topic -> "twitter_stream"
```shell
$ bin/kafka-topic.sh --zookeeper zookeeper:2181 --create --topic twitter_stream --partitions 3 --replication-factor 3
```
STEP4: Test Kafka Cluster 
```shell
bin/kafka-console-producer.sh --broker-list localhost:9092 --topic twitter_stream
bin/kafka-console-consumer.sh --zookeeper zookeeper:2181 --topic twitter_stream
```


