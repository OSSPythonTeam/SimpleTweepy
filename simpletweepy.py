from tkinter import *
from tkinter import messagebox, filedialog
from tkinter import font
import tkinter
from typing import Sized
import tweepy
from tweepy import *
from tweepy import API
from tweepy import user
from tweepy import client
from PIL import Image
import pandas as pd

from tweepy.SimpleTimeLine import simple_timeline
from tweepy.simpleAuth import simpleAuth
from tweepy.simpleSearch import simple_tweet_result
from tweepy.simpleUser import simple_user_result

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
consumer_key = ""
consumer_secret = ""

access_token = ""
access_token_secret = ""

api = simpleAuth(consumer_key, consumer_secret, access_token, access_token_secret)

api.verify_credentials().name
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


temp = api.get_settings()
id = "@" + temp["screen_name"]
temp = api.get_user(screen_name=id)

myinfo = {"name": temp.name, "ID": id, "description": temp.description,
          "creation": temp.created_at, "Followers": temp.following if temp.following else 0,
          "tweets": temp.statuses_count}

searchdata = pd.DataFrame(columns=['name', 'text'])


def search_click():
    search = search_bar.get(1.0, END)
    screenName = search

    if search[0] == "#":

        # simpleSearch
        result = simple_tweet_result(api, search[1:])

        # GUI setting
        lists.pack(side=LEFT, fill=X, expand=True)
        lists.config(yscrollcommand=scr.set)
        lists.delete(0, END)
        for x in result:
            lists.insert(END, str(x))

    elif search[0] == "@":

        # simpleUser
        userinfo = simple_user_result(api, screenName)

        # simpleTimeLine
        result = simple_timeline(api, screenName)

        # lists.pack(side=LEFT, fill=X, expand=True)
        # lists.config(yscrollcommand=tscr.set)
        # lists.delete(0, END)
        timeline_lists.pack(side=LEFT, fill=X, expand=True)
        timeline_lists.config(yscrollcommand=tscr.set)
        timeline_lists.delete(0, END)
        for x in result:
            timeline_lists.insert(END, str(x))
            #lists.insert(END, str(x))

        def send_dm():
            try:
                api.send_direct_message(
                    recipient_id=userinfo["recipient_id"], text=dm_text.get("1.0", END))
            except:
                print("해당 유저에게는 DM을 보낼 수 없습니다.")

        def follow_click():

            if userinfo["following"] == False:
                api.create_friendship(screen_name=str(userinfo["ID"]))
                follow_btn.configure(text="following")
                userinfo["following"] = True
                messagebox.showinfo("follow", str(userinfo["name"]) + " : 팔로우하였습니다!")

            else:
                api.destroy_friendship(screen_name=str(userinfo["ID"]))
                follow_btn.configure(text="follow")
                userinfo["following"] = False
                messagebox.showinfo("follow", str(
                    userinfo["name"]) + " : 팔로우를 취소하였습니다")

        def spam_click():
            try:
                spam = messagebox.askyesno("spam", "신고하시겠습니까?")
                if spam == 'yes':
                    api.report_spam(screen_name=user.screen_name)
            except:
                print("error")

        def block_click():
            api.create_block(screen_name=str(userinfo["ID"]))

        # GUI setting
        screenL = Label(userFrame, text=str(screenName),
                        bg="Gray", anchor=NW, height=11, fg="white", font="Consolas")
        nameL = Label(userFrame, text=str(userinfo["name"]), anchor=W, padx=0)
        followersL = Label(userFrame, text=str(
            userinfo["Followers"]) + "  Followers", anchor=W)
        introduceL = Label(userFrame, text=str(userinfo["description"]), anchor=SW)
        creationL = Label(userFrame, text=str(userinfo["creation"]), anchor=W)
        tweet_countL = Label(userFrame, text=str(userinfo["tweets"]) + "  tweets")

        nameL.configure(font=("Helvetica 27"))
        screenL.configure(font=("Helvetica 10"))
        introduceL.configure(font=("Helvetica 10"))
        creationL.configure(font=("Helvetica 9"))
        followersL.configure(font=("Helvetica 9 bold"))
        tweet_countL.configure(font=("Helvetica 9 bold"))

        nameL.pack()
        screenL.pack()
        introduceL.pack()
        creationL.pack()
        followersL.pack()
        tweet_countL.pack()

        nameL.place(x=5, y=50, width=300, height=45)
        screenL.place(x=1, y=95, width=342, height=25)
        introduceL.place(x=1, y=130, width=300, height=20)
        creationL.place(x=1, y=170, width=300, height=10)
        followersL.place(x=1, y=190, width=150, height=10)
        tweet_countL.place(x=150, y=190, width=100, height=10)

        follow_btn = Button(userFrame, text="follow",
                            command=follow_click, font="Consolas 10 bold", bg="#F0F8FF")
        block_btn = Button(userFrame, text="block",
                           command=block_click, font="Consolas 10 bold", bg="#F0F8FF")
        spam_btn = Button(userFrame, text="spam", command=spam_click,
                          font="Consolas 10 bold", bg="#F0F8FF", fg="red")

        dm_text = Text(userFrame, bd=1, bg="#ABB2B9", width=200,
                       height=30, font="Helvetica 14", fg="black", relief="raised", border=2, )
        send_btn = Button(userFrame, text="send", command=send_dm,
                          border=1, background="#EAECEE")

        follow_btn.pack()
        block_btn.pack()
        spam_btn.pack()
        dm_text.pack()
        send_btn.pack()

        follow_btn.place(x=5, y=220, width=100, height=30)
        block_btn.place(x=120, y=220, width=100, height=30)
        spam_btn.place(x=235, y=220, width=100, height=30)
        dm_text.place(x=10, y=550, width=320, height=150)
        send_btn.place(x=150, y=700, width=50, height=30)

    else:
        return


def my_info():
    # 트윗 올리기
    def post_tweet():
        api.update_status(status=tweet_text.get("1.0", END))

    # 프로필 업데이트
    def update_info():

        if len(str(update_name.get("1.0", END))) != 0:
            api.update_profile(name=update_name.get("1.0", END))
            myinfo["name"] = update_name.get("1.0", END)
            nameL.configure(text=myinfo["name"], font=(
                "Helvetica 27"), anchor=NW, padx=0)
            update_name.delete("1.0", END)

        if len(str(update_description.get("1.0", END))) != 0:
            api.update_profile(description=update_description.get("1.0", END))
            myinfo["description"] = update_description.get("1.0", END)
            introduceL.configure(
                text=myinfo["description"], font=("Helvetica 10"), anchor=NW)
            update_description.delete("1.0", END)

    screenL = Label(myFrame, text=str(myinfo["ID"]),
                    bg="Gray", anchor=NW, height=11, fg="white")
    nameL = Label(myFrame, text=str(myinfo["name"]), anchor=W, padx=0)
    followersL = Label(myFrame, text=str(
        myinfo["Followers"]) + "  Followers", anchor=W)
    introduceL = Label(myFrame, text=str(myinfo["description"]), anchor=SW)
    creationL = Label(myFrame, text=str(myinfo["creation"]), anchor=W)
    tweet_countL = Label(myFrame, text=str(myinfo["tweets"]) + "  tweets")

    update_name = Text(myFrame, width=200, height=25)
    update_name.insert(END, "name")
    update_description = Text(myFrame, width=200, height=50)
    update_description.insert(END, "description")
    saveInfo_btn = Button(myFrame, text="save", command=update_info)

    nameL.configure(font=("Helvetica 27"))
    screenL.configure(font=("Helvetica 10"))
    introduceL.configure(font=("Helvetica 10"))
    creationL.configure(font=("Helvetica 9"))
    followersL.configure(font=("Helvetica 9 bold"))
    tweet_countL.configure(font=("Helvetica 9 bold"))

    nameL.pack()
    screenL.pack()
    introduceL.pack()
    creationL.pack()
    followersL.pack()
    tweet_countL.pack()
    saveInfo_btn.pack()
    update_name.pack()
    update_description.pack()

    nameL.place(x=5, y=50, width=300, height=45)
    screenL.place(x=1, y=95, width=342, height=25)
    introduceL.place(x=1, y=130, width=300, height=20)
    creationL.place(x=1, y=170, width=300, height=10)
    followersL.place(x=1, y=190, width=150, height=10)
    tweet_countL.place(x=150, y=190, width=100, height=10)

    saveInfo_btn.place(x=1, y=230, width=50, height=75)
    update_name.place(x=51, y=230, width=290, height=25)
    update_description.place(x=51, y=255, width=290, height=50)

    tweet_text = Text(myFrame, bd=1, bg="#ABB2B9", width=200,
                      height=30, font="Helvetica 14", fg="black", relief="raised", border=2, )
    tweet_text.insert(END, "What's happening?")
    post_btn = Button(myFrame, text="post", command=post_tweet,
                      border=1, background="#EAECEE")

    tweet_text.pack()
    post_btn.pack()

    tweet_text.place(x=10, y=550, width=320, height=150)
    post_btn.place(x=150, y=700, width=50, height=30)


# 검색 결과 저장
def save_result():
    global searchdata

    search = search_bar.get(1.0, END)
    keyword = search[1:]
    tweets = api.search_tweets(keyword)

    saveL = Label(root, text="", anchor=W, padx=0)
    saveL.configure(font=("Helvetica 14"))
    saveL.pack()
    saveL.place(x=390, y=800, width=360, height=25)

    if idvar.get():
        temp = []
        for i in range(1, 7):
            for tweet in tweets:
                temp.append(str(tweet.author.name))

        searchdata['name'] = temp

    if textvar.get():
        temp = []
        for i in range(1, 7):
            for tweet in tweets:
                temp.append(tweet.text)

        searchdata['text'] = temp

    if timevar.get():
        temp = []
        for i in range(1, 7):
            for tweet in tweets:
                temp.append(str(tweet.created_at))
                # searchdata = searchdata.assign(time=str(tweet.created_at))
                # searchdata['time'] = pd.Series([str(tweet.created_at)])

        searchdata['time'] = temp

    if retweetvar.get():
        temp = []
        for i in range(1, 7):
            for tweet in tweets:
                temp.append(tweet.retweet_count)
                # searchdata['retweet'] = pd.Series(tweet.retweet_count)
                # searchdata = searchdata.fillna(value=0)

        searchdata['retweet'] = temp

    if likevar.get():
        temp = []
        for i in range(1, 7):
            for tweet in tweets:
                temp.append(tweet.favorite_count)
                # searchdata['like'] = pd.Series([tweet.favorite_count])
                # searchdata = searchdata.fillna(value=0)

        searchdata['like'] = temp

    dir = Tk()
    dir.withdraw()
    dir.dirName = filedialog.askdirectory()
    print(dir.dirName)

    if savevar.get() == "xlsx":
        searchdata.to_excel(dir.dirName + '/' + file_name.get("1.0", END + '-1c') + '.xlsx')
        saveL.config(text=dir.dirName + "에 저장했습니다.")

    elif savevar.get() == "csv":
        searchdata.to_csv(dir.dirName + '/' + file_name.get("1.0", END + '-1c') + 'c.csv', index=False)
        saveL.config(text=dir.dirName + "에 저장했습니다.")


#  searchdata = searchdata.append(
#                 {'name': str(tweet.author.name),
#                 'text': tweet.text}, ignore_index=True)


font.Font = "Helvetica 14"
root = Tk()
root.title('simpletweepy')
root.geometry('1200x910')
root.resizable(False, False)

# title bar
label = Label(root, text="simpletweepy", width=1200, height=60,
              fg="White", bg="#17202A", relief=GROOVE, border=3)
label.configure(font=("Helvetica", 20, "italic"))
label.pack()
label.place(x=0, y=0, height=70, width=1200)

# bottom bar
bottomlabel = Label(root, text="공개SW 1조 (일조하조)", width=1200, height=50,
                    fg="White", bg="#17202A")
bottomlabel.configure(font="10", anchor=E)
bottomlabel.pack()
bottomlabel.place(x=0, y=870, height=50, width=1200)

# 검색바
search_bar = Text(root, bd=1, bg="#ABB2B9", width=200,
                  height=30, font="Helvetica 14", fg="Black", relief="raised", border=2,
                  )
search_bar.place(x=910, y=33, height=30, width=240)

# 검색 버튼
pt = PhotoImage(file="photo/search.png")
search_btn = Button(root, image=pt, border=0, command=search_click)
search_btn.pack()
search_btn.place(x=1160, y=30)

# 순서대로 user,검색결과(트윗),나
userFrame = Frame(root, relief=SOLID, bd=3)
searchFrame = Frame(root, relief=SOLID, bd=3)
myFrame = Frame(root, relief=SOLID, bd=3)
timelineFrame = Frame(root,relief=SOLID, bd=3)

title_Image = PhotoImage(file="photo/twitter.png")
title_Img = Label(root, image=title_Image, bg="#17202A")
title_Img.pack()
title_Img.place(x=475,y=20)


userFrame.pack()
searchFrame.pack()
myFrame.pack()
timelineFrame.pack()

userFrame.place(x=20, y=90, width=350, height=760)
searchFrame.place(x=390, y=90, width=420, height=600)
myFrame.place(x=830, y=90, width=350, height=760)
timelineFrame.place(x=30,y=350,width=330, height=280)
#  user_box = Frame(root, relief=SOLID, bd=2)
#     user_box.pack()
#     user_box.place(x=20, y=150, width=600, height=500)


# 트윗 검색 결과 부분 (스크롤)
scr = Scrollbar(searchFrame)
scr.pack(side=RIGHT, fill=Y)

lists = Listbox(searchFrame, width=50, height=400,
                relief="raised", background="White")

# 유저 타임라인 결과 부분 (스크롤)
tscr = Scrollbar(timelineFrame)
tscr.pack(side=RIGHT, fill=Y)

timeline_lists = Listbox(timelineFrame, width=0, height=400,
                relief="raised", background="White")

# 프레임에 내 계정 정보 띄우기
my_info()

# 체크버튼 (저장할 항목)
#  - - - - - - - - - - - - - - - - - - - - - -
idvar = BooleanVar()
textvar = BooleanVar()
timevar = BooleanVar()
retweetvar = BooleanVar()
likevar = BooleanVar()

id_chk = Checkbutton(root, text="ID", variable=idvar)
text_chk = Checkbutton(root, text="text", variable=textvar)
time_chk = Checkbutton(root, text="time", variable=timevar)
retweet_chk = Checkbutton(root, text="retweet", variable=retweetvar)
like_chk = Checkbutton(root, text="like", variable=likevar)

id_chk.pack()
text_chk.pack()
time_chk.pack()
retweet_chk.pack()
like_chk.pack()

id_chk.place(x=410, y=700)
# id_chk.select()
text_chk.place(x=480, y=700)
# text_chk.select()
time_chk.place(x=565, y=700)
retweet_chk.place(x=650, y=700)
like_chk.place(x=740, y=700)

# 라디오버튼 (저장할 파일 확장자 선택)
#  - - - - - - - - - - - - - - - - - - - - - -
savevar = StringVar()

xlsx_chk = Radiobutton(root, text=".xlsx", variable=savevar, value="xlsx")
csv_chk = Radiobutton(root, text=".csv", variable=savevar, value="csv")
#기본값
xlsx_chk.select()

xlsx_chk.pack()
csv_chk.pack()

xlsx_chk.place(x=410, y=770)
csv_chk.place(x=480, y=770)
#  - - - - - - - - - - - - - - - - - - - - - -


# 저장할 파일 이름
file_name = Text(root, bd=1, bg="#ABB2B9", width=300,
                 height=30, font="Helvetica 14", fg="White", insertbackground="White", relief="raised", border=2)
file_name.place(x=390, y=730, height=30, width=360)

# 파일 저장 버튼
file_save_btn = Button(
    root, text="SAVE", command=save_result, border=1, background="#EAECEE")
file_save_btn.pack()
file_save_btn.place(x=750, y=730, width=60, height=30)

root.mainloop()
