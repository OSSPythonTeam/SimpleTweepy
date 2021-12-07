# import the module
import json
import requests
import logging
import Wallpaper
from tweepy.simpleAuth import simpleAuth

consumer_key = ""
consumer_secret = ""

access_token = ""
access_token_secret = ""

api = simpleAuth(consumer_key, consumer_secret, access_token, access_token_secret)

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)
logger.setLevel(logging.INFO)


# 외부 API 불러오기
def get_Cat():
    url = "https://api.thecatapi.com/v1/images/search"

    try:
        response = requests.get(url)
    except:
        logger.info("Error while calling API...")

    res = json.loads(response.text)
    print(res)
    print(res[0]["url"])
    return res[0]["url"]


# 마지막 트윗 정보 확인
def get_last_tweet(file):
    f = open(file, 'r')
    lastId = int(f.read().strip())
    f.close()
    return lastId


# 마지막 트윗 아이디 파일에 쓰기
def put_last_tweet(file, Id):
    f = open(file, 'w')
    f.write(str(Id))
    f.close()
    logger.info("Updated the file with the latest tweet Id")
    return


# 자동 응답
def respondToTweet(file='tweet_ID.txt'):
    last_id = get_last_tweet(file)
    mentions = api.mentions_timeline(since_id=last_id, tweet_mode='extended')
    if len(mentions) == 0:
        return

    new_id = 0
    logger.info("someone mentioned me...")

    for mention in reversed(mentions):
        logger.info(str(mention.id) + '-' + mention.full_text)
        new_id = mention.id
        print("id : ")
        print(new_id)

        if '#cat' in mention.full_text.lower():
            logger.info("Responding back with Cat to -{}".format(mention.id))
            try:
                tweet = get_Cat()
                Wallpaper.get_wallpaper(tweet)

                media = api.media_upload(filename="created_image.png")

                logger.info("liking and replying to tweet")

                api.create_favorite(mention.id)

                api.update_status('@' + mention.user.screen_name + " Here's your Cat",
                                  media_ids=[media.media_id])
            except:
                logger.info("Already replied to {}".format(mention.id))

    put_last_tweet(file, new_id)


if __name__ == "__main__":
    respondToTweet()
