from urllib import request
from typing import List
from datetime import date
import json
import os
from src.atcoder import UserInfo


MAX_USER_COUNT = 5
NUM_DICT = {
    1: "one",
    2: "two",
    3: "three",
    4: "four",
    5: "five"
}

def post_slack_from_userinfo(userinfos: List[UserInfo]):
    blocks = list()
    blocks.append(header_block())
    blocks += ac_ranking_blocks(userinfos)
    blocks.append(footer_block())
    post_message(blocks)


def header_block():
    today_str = date.today().strftime("%Y/%m/%d")
    block = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": f"【{today_str}】AtCoderのランキングだよ\n"
        }
    }
    return block


def ac_ranking_blocks(userinfos: List[UserInfo]):
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
            "type": "plain_text",
            "text": f":{NUM_DICT[i + 1]}:  {info['user_id']}",
            "emoji": True
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


def footer_block():
    block = {
        "type": "section",
        "text": {
            "type": "plain_text",
            "text": "今日も精進しましょー:muscle::muscle::muscle:",
            "emoji": True
        }
    }
    return block


def post_message(blocks):
    data = json.dumps({"blocks": blocks}).encode()
    headers = {"Content-type": "application/json"}
    req = request.Request(
        url=os.getenv("SLACK_INCOMING_WEBHOOK_URL"),
        data=data,
        headers=headers)
    request.urlopen(req)