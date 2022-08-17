# import string
from flask import request
from flask_jwt import jwt_required
from flask_restful import Resource, reqparse

parser = reqparse.RequestParser()
parser.add_argument('name', required=True,
                    help="is required")
parser.add_argument('price', type=float, required=True,
                    help="is required and must be a float!")

items = [
    {
        'id': 'aaa',
        'name': 'first_item',
        'price': 12.99,
    },
    {
        'id': 'aab',
        'name': "second_item",
        'price': 99.99,
    },
]


def reset_items():
    global items
    items = [
        {
            'id': 'aaa',
            'name': 'first_item',
            'price': 12.99,
        },
        {
            'id': 'aab',
            'name': "second_item",
            'price': 99.99,
        },
    ]


class Home(Resource):
    def get(self):
        return {'message': "Hello, flaskers"}


class Items(Resource):
    def get(self):
        return items

    def post(self):
        newItem = parser.parse_args()
        addedItem = {
            'id': 'yya',
            "name": newItem['name'],
            "price": newItem['price'],
        }
        items.append(addedItem)
        payload = {
            'message': "Successfully added!",
            'data': items[-1]
        }
        return payload


class Item(Resource):
    def get(self, id):
        theItemList = [item for item in items if item['id'] == id]
        if len(theItemList) > 0:
            return theItemList[0]

        return None, 404

    def delete(self, id):
        global items
        theItemList = [item for item in items if item['id'] != id]
        items = theItemList
        return {"message": "successfully deleted!"}

    def put(self, id):
        global items
        data = request.get_json()

        theItem = next((item for item in items if item['id'] == id), None)
        if theItem:
            theItem.update(data)
            return {'message': "Update successful!"}

        return {'error': f"item '{id}' could not be updated!"}, 404


class SecretItems(Resource):
    def __init__(self):
        self.items = [
            {
                'id': 'xxx',
                'name': 'first_secret_item',
                'price': 29.99
            },
            {
                'id': 'xxy',
                'name': '2nd_secret_item',
                'price': 59.99
            }
        ]

    @jwt_required()
    def get(self):
        return self.items