import tweepy


def simple_timeline(api, screenName):
    try:
        result = []
        for status in tweepy.Cursor(api.user_timeline, screen_name=screenName, tweet_mode="extended").items(100):
            print(f"{i}번 째 트윗 :" + status.full_text)
            result.append(f"{i}번 째 트윗 :" + status.full_text)

        return result
    except:
        print("error")
