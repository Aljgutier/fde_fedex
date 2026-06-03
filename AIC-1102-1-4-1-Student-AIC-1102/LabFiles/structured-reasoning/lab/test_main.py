from main import main


def test_main_returns_greeting():
    result = main("config.yaml")
    assert result == "Hello, World!"
