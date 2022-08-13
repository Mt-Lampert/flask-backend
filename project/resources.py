from curses import newwin
import string
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
