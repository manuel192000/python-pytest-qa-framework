import pytest

import qa_framework


def test_package_exposes_version():
    assert qa_framework.__version__ == "0.1.0"


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        (1, 2, 3),
        (0, 0, 0),
        (-1, 1, 0),
    ],
)
def test_addition(a, b, expected):
    assert a + b == expected
