from flask import Flask, jsonify


def default_app():
    myApp = Flask(__name__)

    @myApp.route('/')
    def home():
        return jsonify({"message": "Hello, flaskers"})

    return myApp
