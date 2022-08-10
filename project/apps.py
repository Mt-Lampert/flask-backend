from flask import Flask, abort, jsonify, request

stores = [
    {
        'id': 'aaa',
        'name': "first_store",
        'items': [
            {
                'name': 'My Item',
                'price': 15.99,
            }
        ]
    }
]


def default_app():
    myApp = Flask(__name__)

    @myApp.route('/')
    def home():
        return jsonify({"message": "Hello, flaskers"})

    @myApp.route('/stores')
    def get_stores():
        return jsonify(stores)

    @myApp.route('/stores/<string:id>')
    def get_store_by_id(id):
        for store in stores:
            if store['id'] == id:
                return jsonify(store)

        # implicit else => not found: status == 204, no 
        return '', 204

    @myApp.route('/stores/<string:id>/items')
    def get_items_by_store_id(id):
        for store in stores:
            if store['id'] == id:
                return jsonify(store['items'])

        # implicit else => not found: status == 204, no content
        return '', 204

    @myApp.route('/stores', methods=["POST"])
    def add_store():
        req_data = request.get_json()
        new_store = {
            'id': 'zza',
            'name': req_data['name'],
            'items': req_data['items']
        }

        stores.append(new_store)
        myResponse = {
            'message': 'Successfully added!',
            'data': stores[-1],
        }

        return jsonify(myResponse)

    return myApp
