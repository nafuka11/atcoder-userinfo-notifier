from urllib import request
import gzip
import json
from dataclasses import dataclass

ATCODER_ENDPOINT_URL = "https://kenkoooo.com/atcoder/atcoder-api/v2/user_info?user="


@dataclass
class UserInfo:
    user_id: str
    accepted_count: int
    accepted_count_rank: int
    rated_point_sum: float
    rated_point_sum_rank: int


def fetch_atcoder_userinfo(userid: str) -> dict:
    """useridからuserinfoを取得する

    Args:
        userid (str): AtCoderのuserid

    Returns:
        dict: userinfo

    """
    headers = {
        "Accept-Encoding": "gzip"
    }
    req = request.Request(url=ATCODER_ENDPOINT_URL + userid,
                          headers=headers)
    res = request.urlopen(req)
    data = gzip.decompress(res.read())

    return json.loads(data)
