from project import *



if __name__ == "__main__":
    app = restful_app()
    app.run(port=4000, debug=True)
