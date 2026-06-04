from log_tools.reader import count_by_level, list_log_files, search

LOG_DIR = "sample_logs"


def test_list_log_files():
    assert "app.log" in list_log_files(LOG_DIR)


def test_search_redis_errors():
    results = search(LOG_DIR, r"redis", level="ERROR")
    assert len(results) >= 2


def test_count_by_level():
    counts = count_by_level(LOG_DIR)
    assert counts["ERROR"] > 0
    assert counts["INFO"] > 0
