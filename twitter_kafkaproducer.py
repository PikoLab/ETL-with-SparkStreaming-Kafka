import tweepy
from kafka import KafkaProducer
import json
import secrets 


#Streaming With Tweepy<Step1>: Authentication Information
class TwitterAuthenticator():

	def authenticate_twitter_app(self):
		auth = tweepy.OAuthHandler(secrets.consumer_key, secrets.consumer_secret)
		auth.set_access_token(secrets.access_token, secrets.access_token_secret)
		return auth


#Streaming With Tweepy<Step2>:Creating Twitter Stream Listener
class TwitterStreamListener(tweepy.StreamListener):

	def on_data(self, data):
		msg = json.loads(data)
		print('new message')
		
		try:
			if "extended_tweet" in msg: 
				user=str(msg['user']['id'])
				message=str(msg['extended_tweet']['full_text'])
				producer.send(topic, key=bytes(user,'utf8'),value=bytes(message,'utf8'))
			else:
				user=str(msg['user']['id'])
				message=str(msg['text'])
				producer.send(topic, key=bytes(user,'utf8'),value=bytes(message,'utf8'))
			return True

		
		except BaseException as e:
			print('Error on_data: {}'.formart(str(e)))

		return True 


	def on_error(self, status_code):
		if status_code==420:
			return False 
		print (status_code)


#Streaming With Tweepy<Step3>:Creating and Starting a Stream
class TwitterStreamer():

	def __init__(self):
		self.twitter_authenticator=TwitterAuthenticator()


	def get_tweets(self, keyword_list):
		auth=self.twitter_authenticator.authenticate_twitter_app()
		listener=TwitterStreamListener()
		stream = tweepy.Stream(auth = auth, listener=listener)
		stream.filter(track=keyword_list, languages=["en"])
		return stream


if __name__ == "__main__" :
	
	#Create Kafka Producer
	topic="twitter_stream"
	bootstrap_servers="zookeeper:9092, zookeeper:9093"
	producer=KafkaProducer(bootstrap_servers=bootstrap_servers) 


	#tracking FAANG 
	keyword_list=['$AAPL','$GOOG','$GOOGL','$FB','$AMZN','$NFLX']


	#Creating and Starting a Stream
	twitter_streamer=TwitterStreamer()
	twitter_streamer.get_tweets(keyword_list)