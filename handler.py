from urllib import error
from datetime import date
import time
from src.atcoder import fetch_atcoder_userinfo
from src.slack import post_slack_from_userinfo

USER_LIST_FILE = "userlist.txt"


def handle(event, context):
    userinfos = list()
    with open(USER_LIST_FILE) as f:
        for line in f.readlines():
            try:
                userinfos.append(fetch_atcoder_userinfo(line))
                # APIアクセスのたびに1秒Sleepする
                time.sleep(1)
            except error.HTTPError as e:
                print(f"[ERROR] {line}: {e}")
    post_slack_from_userinfo(userinfos, date.today())
