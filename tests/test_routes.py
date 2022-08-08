
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
