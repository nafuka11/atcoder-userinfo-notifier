import pytest
from urllib.error import HTTPError
from src.main import *


@pytest.fixture
def userid_file(tmpdir):
    """Returns userid list filepath"""
    file = tmpdir / "test_file.txt"
    file.write("""
user_id1
user_id2
user_id3
""")
    return str(file)


class TestFetchAtcoderUserinfos:
    params_http_error = {
        "1 error in 3 users": (
            [
                "user_id1",
                "user_id2",
                "user_id3"
            ],
            [
                {
                    "user_id": "user_id1",
                    "accepted_count": 1,
                    "accepted_count_rank": 2345,
                    "rated_point_sum": 345678.0,
                    "rated_point_sum_rank": 4567
                }, {
                    "user_id": "user_id3",
                    "accepted_count": 1,
                    "accepted_count_rank": 2345,
                    "rated_point_sum": 345678.0,
                    "rated_point_sum_rank": 4567
                }
            ]
        )
    }

    @pytest.mark.parametrize("userids, expected",
                             params_http_error.values(),
                             ids=list(params_http_error.keys()))
    def test_http_error(self, mocker, userids, expected):
        """If HTTPError raises, the function should not get dict"""
        def mock_fetch_atcoder_userinfo(userid):
            """The function for fetch_atcoder_userinfo()"""
            if userid == "user_id2":
                raise HTTPError("http://example.com", 500, "Internal Server Error", None, None)
            userinfo = {
                "user_id": userid,
                "accepted_count": 1,
                "accepted_count_rank": 2345,
                "rated_point_sum": 345678.0,
                "rated_point_sum_rank": 4567
            }
            return userinfo

        mocker.patch("src.main.fetch_atcoder_userinfo", side_effect=mock_fetch_atcoder_userinfo)
        mocker.patch("src.main.read_userid_list", return_value=userids)
        actual = fetch_atcoder_userinfos("dummy.txt")
        assert actual == expected


class TestReadUseridList:
    def test_equivant(self, userid_file):
        """Make sure the function returns a correct user_id list"""
        expected = ["user_id1", "user_id2", "user_id3"]
        actual = read_userid_list(userid_file)
        assert actual == expected

    def test_file_not_found(self):
        """If userid file is not found, raises FileNotFoundError"""
        with pytest.raises(FileNotFoundError):
            read_userid_list("not_found_file.txt")
