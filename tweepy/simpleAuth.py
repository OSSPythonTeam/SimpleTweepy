import tweepy


def simpleAuth(key, secret_Key, token, secret_Token):
    consumer_key = key
    consumer_secret = secret_Key
    access_token = token
    access_token_secret = secret_Token

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth, wait_on_rate_limit=True)

    try:
        api.verify_credentials()
        print("인증 완료")
        return api
    except:
        print("인증 오류")
