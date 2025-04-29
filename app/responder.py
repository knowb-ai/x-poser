import tweepy
from app.config import Config

auth = tweepy.OAuth1UserHandler(
    Config.TWITTER_API_KEY,
    Config.TWITTER_API_SECRET,
    Config.TWITTER_ACCESS_TOKEN,
    Config.TWITTER_ACCESS_SECRET,
)
api = tweepy.API(auth)


def reply_to_tweet(tweet_id: str, text: str):
    api.update_status(
        status=text, in_reply_to_status_id=tweet_id, auto_populate_reply_metadata=True
    )
