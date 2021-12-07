userinfo = {"name": "", "ID": "", "description": "",
            "creation": "", "Followers": "", "tweets": "", "recipient_id": "", "profile_image_url": "", "following": ""}


def simple_user_result(api, screenName):
    try:
        user = api.get_user(screen_name=screenName)

        userinfo["name"] = user.name
        userinfo["creation"] = user.created_at
        userinfo["description"] = user.description
        userinfo["ID"] = user.screen_name
        userinfo["tweets"] = user.statuses_count
        userinfo["Followers"] = user.followers_count
        userinfo["recipient_id"] = user.id
        userinfo["profile_image_url"] = user.profile_image_url_https
        userinfo["following"] = user.following

        print("name : " + userinfo["name"])
        print("creation : " + str(userinfo["creation"]))
        print("description : " + userinfo["description"])
        print("ID : " + userinfo["ID"])
        print("tweets : " + str(userinfo["tweets"]))
        print("Followers : " + str(userinfo["Followers"]))
        print("recipient_id : " + str(userinfo["recipient_id"]))
        print("profile_image_url : " + str(userinfo["profile_image_url"]))

        return userinfo

    except:
        print("사용자가 없습니다")