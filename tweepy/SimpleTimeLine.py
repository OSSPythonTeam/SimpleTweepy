import tweepy


def simple_timeline(api, screenName):
    try:
        result = []   # 크롤링 텍스트를 저장 할 리스트 변수
        i = 1
        # item 뒤에 값으로 출력 개수 설정
        for status in tweepy.Cursor(api.user_timeline, screen_name=screenName, tweet_mode="extended").items(30):
            print(f"{i}번 째 트윗 :" + status.full_text)
            result.append(f"{i}번 째 트윗 :" + status.full_text)
            i += 1

        return result

    except:
        print("error")
