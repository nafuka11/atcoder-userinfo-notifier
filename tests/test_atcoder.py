import pytest
import gzip
import json
from urllib.error import HTTPError
from pytest_mock import MockFixture
from src.atcoder import fetch_atcoder_userinfo


@pytest.fixture
def atcoder_api_request_valid(mocker: MockFixture) -> None:
    """urllib.request.urlopen()をモック。当該関数コール時にresponse_dictを返す

    Args:
        mocker (MockFixture): モックフィクスチャ

    """
    response_dict = {
        "user_id": "user_id",
        "accepted_count": 123456,
        "accepted_count_rank": 2345,
        "rated_point_sum": 345678.0,
        "rated_point_sum_rank": 4567
    }
    urlopen_mock = mocker.patch("urllib.request.urlopen")
    urlopen_mock.return_value.read.return_value = gzip.compress(json.dumps(response_dict).encode("utf-8"))


@pytest.fixture
def atcoder_api_request_invalid(mocker: MockFixture) -> None:
    """urllib.request.urlopen()をモック。当該関数コール時にHTTPErrorをraiseする

    Args:
        mocker (MockFixture): モックフィクスチャ

    """
    error = HTTPError("http://example.com", 500, "Internal Server Error", None, None)
    mocker.patch("urllib.request.urlopen", side_effect=error)


class TestFetchAtcoderUserinfo:
    """fetch_atcoder_userinfo()のテスト"""

    def test_equivant(self, atcoder_api_request_valid: None):
        """APIから取得したgzip圧縮JSONを解凍し、dictとして返すことの確認

        Args:
            atcoder_api_request_valid (None): urlopen()をモックするフィクスチャ

        """
        actual = fetch_atcoder_userinfo("user_id")
        expected = {
            "user_id": "user_id",
            "accepted_count": 123456,
            "accepted_count_rank": 2345,
            "rated_point_sum": 345678.0,
            "rated_point_sum_rank": 4567
        }
        assert actual == expected

    def test_error(self, atcoder_api_request_invalid: None):
        """HTTPErrorが発生したとき、そのままraiseされることの確認

        Args:
            atcoder_api_request_invalid (None): urlopen()をモックするフィクスチャ。

        """
        with pytest.raises(HTTPError):
            fetch_atcoder_userinfo("invalid_user_id")
