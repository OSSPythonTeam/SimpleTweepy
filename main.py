import tweepy
from tweepy.simpleAuth import simpleAuth
from tweepy.simpleTweepy import simpleTweepy

consumer_key = "5yYaTNXHiepbPQgvE3MkPUgid"
consumer_secret = "UccOmYrIsEbvz7awi9mhJXiSecSV4maTvUwjKnAZpi9MaBXqpr"
access_token = "1447980933789863937-Ov7WwmYWXgqDGr2xsliZZbIG4D0aIe"
access_token_secret = "25PfrFoZZ6V0FGp8yn63jik62Rb25o2jBZLq2XQ9TNHpV"

api = simpleAuth(consumer_key, consumer_secret, access_token, access_token_secret)

keyword = 'BTS_twt'
result = simpleTweepy(api, 4, keyword)

print(result)

