from src.atcoder import fetch_atcoder_userinfo
from src.slack import post_slack_from_userinfo
from src.atcoder import UserInfo

USER_LIST_FILE = "userlist.txt"


def handle(event, context):
    userinfos = list()
    with open(USER_LIST_FILE) as f:
        for line in f.readlines():
            try:
                userinfos.append(fetch_atcoder_userinfo(line))
            except Exception as e:
                print(e)
    post_slack_from_userinfo(userinfos)
