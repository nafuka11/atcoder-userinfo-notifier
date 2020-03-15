import pytest
from _pytest.monkeypatch import MonkeyPatch
from pytest_mock import MockFixture
from unittest.mock import MagicMock
from src.slack import *


@pytest.fixture()
def mock_slack_api(mocker: MockFixture, monkeypatch: MonkeyPatch) -> MagicMock:
    """環境変数を設定し、urlopen()のモックオブジェクトを返す

    Args:
        mocker (MockFixture): モックフィクスチャ
        monkeypatch (MonkeyPatch): monkeypatchフィクスチャ

    Returns:
        MagicMock: urlopen()のモックオブジェクト

    """
    monkeypatch.setenv("SLACK_INCOMING_WEBHOOK_URL",
                       "https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX")
    urlopen_mock = mocker.patch("urllib.request.urlopen")
    return urlopen_mock


class TestPostSlackFromUserinfo:
    """post_slack_from_userinfo()の正常系テスト"""

    def test_no_userinfo(self, mock_slack_api: MagicMock):
        """userinfosが空のリストのとき、urlopen()が呼び出されない(=Slackにメッセージが投稿されない)ことの確認

        Args:
            mock_slack_api (MagicMock): urlopen()のモックオブジェクト

        """
        userinfo = list()
        now_date = date(2222, 4, 2)
        post_slack_from_userinfo(userinfo, now_date)

        assert not mock_slack_api.called

    def test_userinfos(self, mock_slack_api: MagicMock):
        """userinfosに要素が存在するとき、urlopen()が呼び出されることの確認

        Args:
            mock_slack_api (MagicMock): urlopen()のモックオブジェクト
        """
        userinfo = [{
                "user_id": "user_id1",
                "accepted_count": 1234,
                "accepted_count_rank": 2345,
                "rated_point_sum": 345678.0,
                "rated_point_sum_rank": 4567
        }, {
                "user_id": "user_id2",
                "accepted_count": 123456,
                "accepted_count_rank": 2345,
                "rated_point_sum": 345678.0,
                "rated_point_sum_rank": 4567
        }]
        now_date = date(2222, 4, 2)
        post_slack_from_userinfo(userinfo, now_date)

        assert mock_slack_api.call_count == 1


class TestCreateSlackMessage:
    """create_slack_message()の正常系テスト"""

    params_userinfo = {
        "1 userinfo": (
            [{
                "user_id": "user_id1",
                "accepted_count": 123456,
                "accepted_count_rank": 2345,
                "rated_point_sum": 345678.0,
                "rated_point_sum_rank": 4567
            }],
            date(2222, 4, 2),
            {"blocks": [{"type": "section", "text": {"type": "mrkdwn", "text": "【2222/04/02】AtCoderのランキングだよ\n"}},
                        {"type": "section",
                         "text": {"type": "plain_text", "text": ":white_flower: AC数ランキング:white_flower:"}},
                        {"type": "section", "fields": [{"type": "mrkdwn", "text": ":one:  *user_id1*"},
                                                       {"type": "mrkdwn", "text": "AC: `123456`    Point: `345678`"}]},
                        {"type": "section",
                         "text": {"type": "plain_text", "text": "今日も精進しましょー:muscle::muscle::muscle:", "emoji": True}}]}
        ),
        "2 userinfos": (
            [{
                "user_id": "user_id1",
                "accepted_count": 1234,
                "accepted_count_rank": 2345,
                "rated_point_sum": 345678.0,
                "rated_point_sum_rank": 4567
            }, {
                "user_id": "user_id2",
                "accepted_count": 123456,
                "accepted_count_rank": 2345,
                "rated_point_sum": 345678.0,
                "rated_point_sum_rank": 4567
            }],
            date(2222, 4, 2),
            {'blocks': [{'type': 'section', 'text': {'type': 'mrkdwn', 'text': '【2222/04/02】AtCoderのランキングだよ\n'}},
                        {'type': 'section',
                         'text': {'type': 'plain_text', 'text': ':white_flower: AC数ランキング:white_flower:'}},
                        {'type': 'section', 'fields': [{'type': 'mrkdwn', 'text': ':one:  *user_id2*'},
                                                       {'type': 'mrkdwn', 'text': 'AC: `123456`    Point: `345678`'},
                                                       {'type': 'mrkdwn', 'text': ':two:  *user_id1*'},
                                                       {'type': 'mrkdwn', 'text': 'AC: `  1234`    Point: `345678`'}]},
                        {'type': 'section',
                         'text': {'type': 'plain_text', 'text': '今日も精進しましょー:muscle::muscle::muscle:', 'emoji': True}}]}
        ),
        "5 userinfos": (
            [{
                "user_id": "user_id1",
                "accepted_count": 1,
                "accepted_count_rank": 2345,
                "rated_point_sum": 345678.0,
                "rated_point_sum_rank": 4567
            }, {
                "user_id": "user_id2",
                "accepted_count": 12,
                "accepted_count_rank": 2345,
                "rated_point_sum": 345678.0,
                "rated_point_sum_rank": 4567
            },  {
                "user_id": "user_id3",
                "accepted_count": 123,
                "accepted_count_rank": 2345,
                "rated_point_sum": 345678.0,
                "rated_point_sum_rank": 4567
            }, {
                "user_id": "user_id4",
                "accepted_count": 1234,
                "accepted_count_rank": 2345,
                "rated_point_sum": 345678.0,
                "rated_point_sum_rank": 4567
            }, {
                "user_id": "user_id5",
                "accepted_count": 12345,
                "accepted_count_rank": 2345,
                "rated_point_sum": 345678.0,
                "rated_point_sum_rank": 4567
            }],
            date(2222, 12, 31),
            {'blocks': [{'type': 'section', 'text': {'type': 'mrkdwn', 'text': '【2222/12/31】AtCoderのランキングだよ\n'}},
                        {'type': 'section',
                         'text': {'type': 'plain_text', 'text': ':white_flower: AC数ランキング:white_flower:'}},
                        {'type': 'section', 'fields': [{'type': 'mrkdwn', 'text': ':one:  *user_id5*'},
                                                       {'type': 'mrkdwn', 'text': 'AC: `12345`    Point: `345678`'},
                                                       {'type': 'mrkdwn', 'text': ':two:  *user_id4*'},
                                                       {'type': 'mrkdwn', 'text': 'AC: ` 1234`    Point: `345678`'},
                                                       {'type': 'mrkdwn', 'text': ':three:  *user_id3*'},
                                                       {'type': 'mrkdwn', 'text': 'AC: `  123`    Point: `345678`'},
                                                       {'type': 'mrkdwn', 'text': ':four:  *user_id2*'},
                                                       {'type': 'mrkdwn', 'text': 'AC: `   12`    Point: `345678`'},
                                                       {'type': 'mrkdwn', 'text': ':five:  *user_id1*'},
                                                       {'type': 'mrkdwn', 'text': 'AC: `    1`    Point: `345678`'}]},
                        {'type': 'section',
                         'text': {'type': 'plain_text', 'text': '今日も精進しましょー:muscle::muscle::muscle:', 'emoji': True}}]}
        ),
        "6 userinfos": (
            [{
                "user_id": "user_id1",
                "accepted_count": 12345,
                "accepted_count_rank": 2345,
                "rated_point_sum": 345678.0,
                "rated_point_sum_rank": 4567
            }, {
                "user_id": "user_id2",
                "accepted_count": 12,
                "accepted_count_rank": 2345,
                "rated_point_sum": 345678.0,
                "rated_point_sum_rank": 4567
            }, {
                "user_id": "user_id3",
                "accepted_count": 123,
                "accepted_count_rank": 2345,
                "rated_point_sum": 345678.0,
                "rated_point_sum_rank": 4567
            }, {
                "user_id": "user_id4",
                "accepted_count": 1234,
                "accepted_count_rank": 2345,
                "rated_point_sum": 345678.0,
                "rated_point_sum_rank": 4567
            }, {
                "user_id": "user_id5",
                "accepted_count": 1,
                "accepted_count_rank": 2345,
                "rated_point_sum": 345678.0,
                "rated_point_sum_rank": 4567
            }, {
                "user_id": "user_id6",
                "accepted_count": 123456,
                "accepted_count_rank": 2345,
                "rated_point_sum": 345678.0,
                "rated_point_sum_rank": 4567
            }],
            date(2222, 12, 31),
            {'blocks': [{'type': 'section', 'text': {'type': 'mrkdwn', 'text': '【2222/12/31】AtCoderのランキングだよ\n'}},
                        {'type': 'section',
                         'text': {'type': 'plain_text', 'text': ':white_flower: AC数ランキング:white_flower:'}},
                        {'type': 'section', 'fields': [{'type': 'mrkdwn', 'text': ':one:  *user_id6*'},
                                                       {'type': 'mrkdwn', 'text': 'AC: `123456`    Point: `345678`'},
                                                       {'type': 'mrkdwn', 'text': ':two:  *user_id1*'},
                                                       {'type': 'mrkdwn', 'text': 'AC: ` 12345`    Point: `345678`'},
                                                       {'type': 'mrkdwn', 'text': ':three:  *user_id4*'},
                                                       {'type': 'mrkdwn', 'text': 'AC: `  1234`    Point: `345678`'},
                                                       {'type': 'mrkdwn', 'text': ':four:  *user_id3*'},
                                                       {'type': 'mrkdwn', 'text': 'AC: `   123`    Point: `345678`'},
                                                       {'type': 'mrkdwn', 'text': ':five:  *user_id2*'},
                                                       {'type': 'mrkdwn', 'text': 'AC: `    12`    Point: `345678`'}]},
                        {'type': 'section',
                         'text': {'type': 'plain_text', 'text': '今日も精進しましょー:muscle::muscle::muscle:', 'emoji': True}}]}
        ),
    }

    @pytest.mark.parametrize("userinfos, now_date, expected",
                             params_userinfo.values(),
                             ids=list(params_userinfo.keys()))
    def test_userinfo(self, userinfos: List[dict], now_date: date, expected: dict):
        """userinfos, now_dateに応じたメッセージ(expected)を返すことの確認

        Args:
            userinfos (List[dict]): 関数に渡す引数(userinfos)
            now_date (date): 関数に渡す引数(now_date)
            expected (dict): 想定される戻り値

        """
        actual = create_slack_message(userinfos, now_date)
        assert actual == expected


class TestPostMessage:
    """post_message()の正常系テスト"""

    def test_equivant(self, mock_slack_api: MagicMock):
        """urlopen()が呼び出され、渡されるパラメータが正しいことの確認

        Args:
            mock_slack_api (MagicMock): urlopen()のモックオブジェクト

        """
        message = {"data": "messages"}

        post_message(message)
        actual = mock_slack_api.call_args.args[0]

        assert actual.get_full_url() == "https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX"
        assert actual.get_header("Content-type") == "application/json"
        assert actual.data == json.dumps(message).encode()


class TestPostMessageException:
    """post_message()の異常系テスト"""

    def test_no_env(self, mock_slack_api: MagicMock, monkeypatch: MonkeyPatch):
        """環境変数が未設定の時、urlopen()が呼び出されないことの確認

        Args:
            mock_slack_api (MagicMock): urlopen()のモックオブジェクト
            monkeypatch (MonkeyPatch): monkeypatchフィクスチャ

        """
        monkeypatch.delenv("SLACK_INCOMING_WEBHOOK_URL")
        message = {"data": "messages"}

        post_message(message)
        assert not mock_slack_api.called
