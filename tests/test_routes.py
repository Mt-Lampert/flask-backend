
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

def test_get_stores(test_client):
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
    
def test_add_store(test_client):
    """
    GIVEN a flask app has been provided
    WHEN we POST a new store to the '/stores' endpoint
    THEN the response status is OK
    AND the response data returns the post we sent
    AND we additionally receive a success message

    Args:
        test_client (Object): Flask app object
    """
    response = test_client.post('/stores', json={
        'name': 'zingboffle', 
        'items': [
            {
                'name': "Fake Diamond",
                'price': 99.99
            }
        ]
    })
    
    assert response.status_code == 200
    assert response.json['data']['name'] == 'zingboffle'
    assert response.json['message'] == "Successfully added!"

def test_get_store_by_id(test_client):
    """
    GIVEN a flask app has been provided
    WHEN we GET a store using '/stores/:id'
    AND the store has been found in the backend
    THEN the response status is OK
    AND the response data returns the store we want

    Args:
        test_client (Object): Flask app object
    """
    response = test_client.get('/stores/aaa')
    assert response.status_code == 200
    assert response.json['name'] == "first_store"
    

def test_get_store_by_id__fail(test_client):
    """
    GIVEN a flask app has been provided
    WHEN we GET a store using '/stores/:name'
    AND the store could not be found in the backend
    THEN the response status is 204 ("No content")

    Args:
        test_client (Object): Flask app object
    """
    response = test_client.get('/stores/xxx')
    assert response.status_code == 204