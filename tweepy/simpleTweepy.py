import tweepy


def simpleTweepy(api, number, keyword):
    # keyword의 사용자의 타임라인?
    if number == 1:
        try:
            tweets = api.user_timeline(screen_name=keyword, count=10)
            return tweets
        except:
            print("유효한 사용자가 없습니다.")

    # 맨션 반환
    if number == 2:
        try:
            tweets = api.mentions_timeline(count=10)
            return tweets
        except:
            print("유효한 사용자가 없습니다.")

    # keyword 검색
    if number == 3:
        result = []
        tweets = api.search_tweets(keyword)
        for tw in tweets:
            result.append(tw.text)

        # print(result[1])
        return result

    # follower 10명 정보 가져오기
    if number == 4:
        try:
            tweets = api.get_followers(screen_name=keyword, count=10)
            return tweets
        except:
            print("유효한 사용자가 없습니다.")

