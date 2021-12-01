import tweepy


def simple_timeline(api, screenName):
    try:
        result = []
        i = 1
        for status in tweepy.Cursor(api.user_timeline, screen_name=screenName, tweet_mode="extended").items(100):
            print(f"{i}번 째 트윗 :" + status.full_text)
            result.append(f"{i}번 째 트윗 :" + status.full_text)
            i += 1

        return result
        # tweets = tweepy.Cursor(api.user_timeline, screen_name=screenName,tweet_mode="extended")
        # print(tweets)
    except:
        print("error")
