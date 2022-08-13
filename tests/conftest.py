import pytest
from project import default_app, restful_app


@pytest.fixture(scope='module')
def test_client():
    flask_app = default_app()
    with flask_app.test_client() as test_client:
        # yield, not return!
        yield test_client
    # with yield, cleanup is possible after yielding ;)


@pytest.fixture()
def restful_client():
    myApp = restful_app()
    with myApp.test_client() as restful_client:
        # yield, not return!
        yield restful_client

    # with yield, cleanup is possible after yielding ;)