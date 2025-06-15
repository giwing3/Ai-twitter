import tweepy from config
import TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET

auth = tweepy.OAuth1UserHandler( TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET ) twitter_api = tweepy.API(auth)

def post_tweet(text): twitter_api.update_status(status=text)
