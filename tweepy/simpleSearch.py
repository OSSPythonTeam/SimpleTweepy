import tweepy


def simple_tweet_result(api,keyword):
    result = []  # 크롤링 텍스트를 저장 할 리스트 변수

    for tweet in tweepy.Cursor(api.search_tweets, keyword).items(30):
        # keyword 검색 실시. 결과가 tweets 변수에 담긴다.

            result.append("ID : " + tweet.author.name)
            result.append([tweet.text])
            result.append("like : " + str(tweet.favorite_count) +
                          "    /    retweet : " + str(tweet.retweet_count))
            result.append("- - - - - - - - - - - - - - - - - -")
    for i in range(1, len(result)):
        print(result[i])

    return result
