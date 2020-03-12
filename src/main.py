from urllib import error
from datetime import date
import time
from typing import List
from src.atcoder import fetch_atcoder_userinfo
from src.slack import post_slack_from_userinfo


def main(user_list_file: str) -> None:
    userinfos = fetch_atcoder_userinfos(user_list_file)
    post_slack_from_userinfo(userinfos, date.today())


def fetch_atcoder_userinfos(user_list_file: str) -> List[dict]:
    """ユーザIDリストファイルから成績を取得する"""
    userinfos = list()
    userids = read_userid_list(user_list_file)
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
