from flask import Flask, jsonify, request

stores = [
    {
        'name': "My wonderful store",
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
    
    @myApp.route('/stores', methods=["POST"])
    def add_store():
        req_data = request.get_json()
        new_store = {
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
