
def test_rootendpoint(restful_client):
    """
    GIVEN a default app has been provided
    WHEN we GET the '/' endpoint
    THEN the response status is OK
    AND we find 'flaskers' in the response
    AND we won't find 'Hallo' in the response
    """
    response = restful_client.get('/')
    assert response.status_code == 200
    assert 'flaskers' in response.json['message']
    assert 'Hallo' not in response.json['message']

def test_get_items(restful_client):
    """
    GIVEN a flask app has been provided
    WHEN we GET the '/items' endpoint
    THEN the response status is OK
    AND the response data is a list
    AND the list is not empty  

    Args:
        restful_client (Object): Flask app object
    """
    response = restful_client.get('/items')
    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert len(response.json) > 0
    
def test_add_store(restful_client):
    """
    GIVEN a flask app has been provided
    WHEN we POST a new item to the '/item' endpoint
    THEN the response status is OK
    AND the response data returns the post we sent
    AND we additionally receive a success message

    Args:
        restful_client (Object): Flask app object
    """
    response = restful_client.post('/items', json={
        'name': 'zingboffle', 
        'price': 49.99
    })
    
    assert response.status_code == 200
    assert response.json['data']['name'] == 'zingboffle'
    assert response.json['message'] == "Successfully added!"

def test_get_item_by_id(restful_client):
    """
    GIVEN a flask app has been provided
    WHEN we GET a store using '/stores/:id'
    AND the store has been found in the backend
    THEN the response status is OK
    AND the response data returns the store we want

    Args:
        restful_client (Object): Flask app object
    """
    response = restful_client.get('/item/aaa')
    assert response.status_code == 200
    assert response.json['name'] == "first_item"
    
def test_get_store_by_id__fail(restful_client):
    """
    GIVEN a flask app has been provided
    WHEN we GET a store using '/items/:id'
    AND the store could not be found in the backend
    THEN the response status is 404 ("Not found")

    Args:
        restful_client (Object): Flask app object
    """
    response = restful_client.get('/stores/xxx')
    assert response.status_code == 404
