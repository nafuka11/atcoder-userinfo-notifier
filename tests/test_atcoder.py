import pytest
import gzip
import json
from urllib.error import HTTPError
from src.atcoder import fetch_atcoder_userinfo


@pytest.fixture
def atcoder_api_request_valid(mocker):
    """urllib.request.urlopen().read() returns gzip-compressed json"""
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
def atcoder_api_request_invalid(mocker):
    """urllib.request.urlopen() throws HTTPError"""
    error = HTTPError("http://example.com", 500, "Internal Server Error", None, None)
    mocker.patch("urllib.request.urlopen", side_effect=error)


class TestFetchAtcoderUserinfo:
    def test_equivant(self, atcoder_api_request_valid):
        """Make sure API response is decompressed
           and decompressed object is correct dict"""
        actual = fetch_atcoder_userinfo("user_id")
        expected = {
            "user_id": "user_id",
            "accepted_count": 123456,
            "accepted_count_rank": 2345,
            "rated_point_sum": 345678.0,
            "rated_point_sum_rank": 4567
        }
        assert actual == expected

    def test_error(self, atcoder_api_request_invalid):
        """<invalid_user_id> throws HTTPError"""
        with pytest.raises(HTTPError):
            fetch_atcoder_userinfo("invalid_user_id")
