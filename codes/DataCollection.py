from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time

consumerKey = 'wb22Y8wyJ5dQZIqcuQQs3TOMr'
consumerSecret = 'sefxdoiTHWCrEBwSWE9zCPSb4VqTIwXe95fCTBk6qi2Y34yor3'
accessToken = '836485825353277440-K6JwZiLRgwtwYlWUIwnykoszckQ08Ps'
accessSecret = 'WFOFTLkaMPLPQoc160RhBKhleI7YmAFXQ0RJzEcOUSP5j'
#Emotion Categories: anger, disgust, fear, guilt, interest, joy, sadness, shame and surprise

class listener(StreamListener):
    def on_data(self, data):
        try:
            #split the tweet and take only text portion of the tweet
            tweet_text = data.split(',"text":"')[1].split('","source')[0]#[1] indicate the right side of the split


            #Skipping Re-Tweets and tweets containing links to other content
            if "RT @" not in tweet_text and "https:" not in tweet_text \
                    and "http:" not in tweet_text and "\\u" not in tweet_text:
                print(tweet_text)
                saving_file = open('../data/tweets', 'a')
                saving_file.write(tweet_text)
                saving_file.write('\n')
                saving_file.close()
                return True
        except BaseException as e:
            print('Failed on data', str(e))
            time.sleep(5)

    def on_error(self, status):
        print(status)

auth = OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessToken, accessSecret)
twitterStream = Stream(auth, listener())
#filter tweet according to keyword
twitterStream.filter(track=["sad"])


