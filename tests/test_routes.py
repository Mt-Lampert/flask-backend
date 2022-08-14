
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

def test_add_store__name_fail(restful_client):
    """
    GIVEN a flask app has been provided
    WHEN we POST a new item to the '/item' endpoint
    AND the new item lacks a 'name' field
    THEN the response status is 404
    AND we get an error message

    Args:
        restful_client (Object): Flask app object
    """
    response = restful_client.post('/items', json={
        'price': 49.99
    })
    assert response.status_code == 400
    assert response.json['message']['name'] == "is required"

def test_add_store__price_fail(restful_client):
    """
    GIVEN a flask app has been provided
    WHEN we POST a new item to the '/item' endpoint
    AND the new item has an invalid 'price' field
    THEN the response status is 404
    AND we get an error message

    Args:
        restful_client (Object): Flask app object
    """
    response = restful_client.post('/items', json={
        'name': "Zingel",
        'price': 'wtf'
    })
    assert response.status_code == 400
    assert 'float' in response.json['message']['price'] 


def test_get_item_by_id(restful_client):
    """
    GIVEN a flask app has been provided
    WHEN we GET a store using '/item/:id'
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
    WHEN we GET a store using '/item/:id'
    AND the store could not be found in the backend
    THEN the response status is 404 ("Not found")

    Args:
        restful_client (Object): Flask app object
    """
    response = restful_client.get('/item/xxx')
    assert response.status_code == 404

def test_delete_item_by_id(restful_client):
    """
    GIVEN a flask app has been provided
    WHEN we DELETE an item using '/item/:id'
    AND the store could be found in the backend
    THEN the response status is 200 
    Args:
        restful_client (Object): Flask app object
    """
    response = restful_client.delete('/item/aab')
    assert response.status_code == 200

    """
    GIVEN an item has been deleted
    WHEN we GET the items using '/items'
    THEN the status is 200
    AND the item list has only one element.
    """
    list_response = restful_client.get('/items')
    assert list_response.status_code == 200
    assert len(list_response.json) == 1
    assert list_response.json[0]['id'] == 'aaa'
