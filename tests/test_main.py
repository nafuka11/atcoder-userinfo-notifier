import pytest
from pathlib import Path
from pytest_mock import MockFixture
from src.main import *


@pytest.fixture
def userid_file(tmp_path: Path) -> str:
    """useridlistファイルのパス文字列を返す

    Args:
        tmp_path (Path): tmp_pathフィクスチャ

    Returns:
        str: useridlistファイルのパス文字列

    """
    file = tmp_path / "test_file.txt"
    file.write_text("""
user_id1
user_id2
user_id3
""")
    return str(file)


@pytest.fixture
def mock_time_sleep(mocker: MockFixture) -> None:
    """テスト中sleepしないよう、time.sleep()をモックする

    Args:
        mocker (MockFixture): モックフィクスチャ

    """
    mocker.patch("time.sleep")


@pytest.mark.usefixtures("mock_time_sleep")
class TestFetchAtcoderUserinfos:
    """fetch_atcoder_userinfos()の正常系テスト"""

    params_http_error = {
        "1 error in 3 users": (
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

    @pytest.mark.parametrize("expected",
                             params_http_error.values(),
                             ids=list(params_http_error.keys()))
    def test_http_error(self, mocker: MockFixture, expected: List[dict], userid_file: str):
        """Userinfo取得でHTTPErrorが発生した場合、エラーをraiseせず処理を続行することの確認

        Args:
            mocker (MockFixture): モックフィクスチャ
            expected (List[dict]): 想定される戻り値。userinfoのリスト
            userid_file (str): useridlistファイルのパス文字列

        """
        def mock_fetch_atcoder_userinfo(userid: str) -> dict:
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
        actual = fetch_atcoder_userinfos(userid_file)
        assert actual == expected

    def test_file_not_found(self):
        """useridlistファイルが見つからなかったとき、空のlistを返すことの確認"""
        actual = fetch_atcoder_userinfos("not_found_file.txt")
        assert actual == list()


class TestReadUseridList:
    """read_userid_list()の正常系テスト"""

    def test_equivant(self, userid_file: str):
        """指定されたパスからuseridのリストを返すことの確認

        Args:
            userid_file (str): useridlistファイルのパス文字列

        """
        expected = ["user_id1", "user_id2", "user_id3"]
        actual = read_userid_list(userid_file)
        assert actual == expected


class TestReadUseridListException:
    """read_userid_list()の異常系テスト"""

    def test_file_not_found(self):
        """指定されたパスが存在しない場合、FileNotFoundErrorがraiseされることの確認"""
        with pytest.raises(FileNotFoundError):
            read_userid_list("not_found_file.txt")
