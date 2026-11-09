import pytest

from qa_framework.validators import is_valid_email, password_errors


@pytest.mark.smoke
def test_default_user_passes_all_rules(make_user):
    user = make_user()

    assert is_valid_email(user["email"])
    assert password_errors(user["password"]) == []


@pytest.mark.regression
@pytest.mark.parametrize(
    "email",
    ["qa@example.com", "first.last@sub.example.org", "a+tag@example.io"],
    ids=["simple", "dotted-subdomain", "plus-tag"],
)
def test_valid_emails_are_accepted(email):
    assert is_valid_email(email)


@pytest.mark.regression
@pytest.mark.parametrize(
    "email",
    ["", "no-at-sign.com", "two@@example.com", "spaces in@example.com", "missing@tld"],
    ids=["empty", "no-at", "double-at", "whitespace", "no-tld"],
)
def test_invalid_emails_are_rejected(email):
    assert not is_valid_email(email)


@pytest.mark.regression
@pytest.mark.parametrize(
    ("password", "expected"),
    [
        ("Short1", ["too_short"]),
        ("longpassword1", ["missing_uppercase"]),
        ("LongPassword", ["missing_digit"]),
        ("short", ["too_short", "missing_digit", "missing_uppercase"]),
    ],
    ids=["too-short", "no-uppercase", "no-digit", "everything-wrong"],
)
def test_password_reports_every_broken_rule(password, expected):
    assert password_errors(password) == expected


def test_overriding_one_field_keeps_the_rest(make_user):
    user = make_user(role="admin")

    assert user["role"] == "admin"
    assert user["email"] == "qa.user@example.com"
