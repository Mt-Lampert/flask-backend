from flask import _request_ctx_stack
from project.auth import User


def _jwt_required_mock(realm='default'):
    _request_ctx_stack.top.current_identity = User(1, "Mario", "abcd")


def test_get_secret_items(mocker, restful_client):
    """
    GIVEN the GET '/secret-items' route is protected using JWT
    WHEN we try to GET the '/secret-items'
    AND we DO mock 'flask_jwt._jwt_required'
    THEN we get response.status_code 200
    AND we have access to the secret items
    """
    mocker.patch(
        # we don't have to import this. path will do.
        'flask_jwt._jwt_required',
        side_effect=_jwt_required_mock
    )
    response = restful_client.get('/secret-items')
    assert response.status_code == 200, response.json
    assert len(response.json) > 0
    assert response.json[0]['price'] == 29.99

def test_get_secret_items__fail(restful_client):
    """
    GIVEN the GET '/secret-items' route is protected using JWT
    WHEN we try to GET the '/secret-items'
    AND we do not mock 'flask_jwt._jwt_required'
    THEN we get an Error instead of status 200
    AND we have no access to the secret items
    """
    response = restful_client.get('/secret-items')
    assert response.status_code != 200
