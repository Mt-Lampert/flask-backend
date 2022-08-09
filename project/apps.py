from flask import Flask, jsonify

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
    def getStores():
        return jsonify(stores)

    return myApp
