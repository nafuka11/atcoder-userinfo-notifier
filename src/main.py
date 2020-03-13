from urllib import error
from datetime import date
import time
from typing import List
from src.atcoder import fetch_atcoder_userinfo
from src.slack import post_slack_from_userinfo


def main(user_list_file: str) -> None:
    userinfos = fetch_atcoder_userinfos(user_list_file)
    try:
        post_slack_from_userinfo(userinfos, date.today())
    except error.HTTPError as e:
        print(f"[ERROR] Failed to post a message to slack: {e}")


def fetch_atcoder_userinfos(user_list_file: str) -> List[dict]:
    """ユーザIDリストファイルから成績を取得する"""
    userinfos = list()
    try:
        userids = read_userid_list(user_list_file)
    except IOError as e:
        print(f"[ERROR] {e}")
        return userinfos
    for userid in userids:
        try:
            userinfos.append(fetch_atcoder_userinfo(userid))
            # APIアクセスのたびに1秒Sleepする
            time.sleep(1)
        except error.HTTPError as e:
            print(f"[ERROR] {userid}: {e}")
    return userinfos


def read_userid_list(user_list_file: str) -> List[str]:
    """ユーザIDリストをファイルから取得する"""
    with open(user_list_file) as f:
        return [line.rstrip() for line in f.readlines() if line.rstrip() != ""]
