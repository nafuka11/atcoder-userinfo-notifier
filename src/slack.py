from urllib import request
from typing import List
from datetime import date
import json
import os

MAX_USER_COUNT = 5
NUM_DICT = {
    1: "one",
    2: "two",
    3: "three",
    4: "four",
    5: "five"
}
SLACK_URL_ENV_NAME = "SLACK_INCOMING_WEBHOOK_URL"

def post_slack_from_userinfo(userinfos: List[dict], now_date: date) -> None:
    """SlackにAtCoderの成績ランキングを投稿する"""
    # ユーザが存在しない場合は、投稿しない
    if len(userinfos) == 0:
        return

    message = create_slack_message(userinfos, now_date)
    post_message(message)


def create_slack_message(userinfos: List[dict], now_date: date) -> dict:
    """Slackに投稿するメッセージを返す"""
    blocks = list()
    blocks.append(header_block(now_date))
    blocks += ac_ranking_blocks(userinfos)
    blocks.append(footer_block())
    return {"blocks": blocks}


def header_block(now_date: date) -> dict:
    """Slackに投稿するメッセージのヘッダ部を返す"""
    today_str = now_date.strftime("%Y/%m/%d")
    block = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": f"【{today_str}】AtCoderのランキングだよ\n"
        }
    }
    return block


def ac_ranking_blocks(userinfos: List[dict]) -> List[dict]:
    """Slackに投稿するメッセージのAC数ランキング部分を返す"""
    blocks = list()

    # header
    block = {
        "type": "section",
        "text": {
            "type": "plain_text",
            "text": ":white_flower: AC数ランキング:white_flower:"
        }
    }
    blocks.append(block)

    # user ranking
    fields = list()
    users = sorted(userinfos, key=lambda u: u["accepted_count"], reverse=True)[:MAX_USER_COUNT]
    max_ac_digit = len(str(users[0]["accepted_count"]))
    max_point_digit = len(str(int(users[0]["rated_point_sum"])))
    for i, info in enumerate(users):
        fields.append({
            "type": "mrkdwn",
            "text": f":{NUM_DICT[i + 1]}:  *{info['user_id']}*"
        })
        fields.append({
            "type": "mrkdwn",
            "text": f"AC: `{info['accepted_count']:>{max_ac_digit}}`    "
                    f"Point: `{int(info['rated_point_sum']):>{max_point_digit}}`"
        })
    blocks.append({
        "type": "section",
        "fields": fields
    })
    return blocks


def footer_block() -> dict:
    """Slackに投稿するメッセージのフッタ部を返す"""
    block = {
        "type": "section",
        "text": {
            "type": "plain_text",
            "text": "今日も精進しましょー:muscle::muscle::muscle:",
            "emoji": True
        }
    }
    return block


def post_message(message: dict) -> None:
    """Slackに指定したblocksをメッセージとして投稿する"""
    data = json.dumps(message).encode()
    headers = {"Content-type": "application/json"}
    url = os.getenv(SLACK_URL_ENV_NAME)
    if url is None:
        print(f"[ERROR] Environment variable does not exist: {SLACK_URL_ENV_NAME}")
        return
    req = request.Request(
        url=url,
        data=data,
        headers=headers)
    request.urlopen(req)
