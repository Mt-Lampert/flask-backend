
def test_rootendpoint(test_client):
    """
    GIVEN a default app has been provided
    WHEN we GET the '/' endpoint
    THEN the response status is OK
    AND we find 'flaskers' in the response
    AND we won't find 'Hallo' in the response
    """
    response = test_client.get('/')
    assert response.status_code == 200
    assert 'flaskers' in response.json['message']
    assert 'Hallo' not in response.json['message']

def test_stores_endpoint(test_client):
    """
    GIVEN a flask app has been provided
    WHEN we GET the '/stores' endpoint
    THEN the response status is OK
    AND the response data is a list
    AND the list is not empty  

    Args:
        test_client (Object): Flask app object
    """
    response = test_client.get('/stores')
    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert len(response.json) > 0