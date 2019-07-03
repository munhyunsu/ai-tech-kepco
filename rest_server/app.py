from flask import Flask, request
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

DRESPONSE = {
}

class ClientInfo(Resource):
    def post(self):
        data = request.get_json()
        print(data)
        return ''

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/')
api.add_resource(ClientInfo, '/clientinfo')

if __name__ == '__main__':
    app.run(debug=True)