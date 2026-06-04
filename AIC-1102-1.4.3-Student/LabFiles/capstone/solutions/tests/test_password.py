from src.password import hash_password, verify_password


def test_hash_roundtrips():
    stored = hash_password("hunter2")
    assert verify_password("hunter2", stored) is True


def test_same_password_produces_different_hashes():
    a = hash_password("hunter2")
    b = hash_password("hunter2")
    assert a != b


def test_verify_rejects_wrong_password():
    stored = hash_password("hunter2")
    assert verify_password("wrong-password", stored) is False


def test_verify_rejects_malformed_stored():
    assert verify_password("anything", "not-a-valid-format") is False


def test_verify_rejects_unknown_algorithm_prefix():
    assert verify_password("anything", "bcrypt$1$2$3$saltb64$hashb64") is False


def test_verify_rejects_empty_string():
    assert verify_password("anything", "") is False


def test_stored_format_has_six_segments():
    stored = hash_password("p")
    assert stored.count("$") == 5


def test_algorithm_prefix_is_scrypt():
    stored = hash_password("p")
    assert stored.startswith("scrypt$")
