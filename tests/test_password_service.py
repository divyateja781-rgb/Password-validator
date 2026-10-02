import pytest

from password_service import validate_password


def test_strong_password_passes_all_rules():
    result = validate_password("Secure@123")
    assert result.is_valid
    assert result.score == 5
    assert result.strength == "Strong"


@pytest.mark.parametrize(
    ("password", "failed_rule"),
    [
        ("Short1!", "length"),
        ("lowercase1!", "uppercase"),
        ("UPPERCASE1!", "lowercase"),
        ("NoNumber!", "number"),
        ("NoSpecial123", "special"),
    ],
)
def test_each_required_rule(password, failed_rule):
    result = validate_password(password)
    failures = {rule.key for rule in result.rules if not rule.passed}
    assert failed_rule in failures
    assert not result.is_valid


def test_empty_password_is_weak():
    result = validate_password("")
    assert result.score == 0
    assert result.strength == "Weak"


def test_four_rules_is_medium():
    result = validate_password("NoSpecial123")
    assert result.score == 4
    assert result.strength == "Medium"

