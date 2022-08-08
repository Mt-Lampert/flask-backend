import pytest
from project import default_app


@pytest.fixture(scope='module')
def test_client():
    flask_app = default_app()
    with flask_app.test_client() as test_client:
        # yield, not return!
        yield test_client

    # with yield, cleanup is possible after yielding ;)
