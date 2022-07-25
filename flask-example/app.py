from flask import Flask
from flask_restful import Api, marshal_with

app = Flask(__name__)
api = Api(app)


class TestClass:
    def get(self):
        return "Hello Test"


api.add_resource(TestClass, "/test")


@app.route("/")
def hello_world():
    return "Hello World!"


if __name__ == "__main__":
    app.run(debug=True)
