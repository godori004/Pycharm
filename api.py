from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

class CreateUser(Resource):
    def post(self):

        return {'status': 'success'}
    def get(self):
        parser = reqparse.RequestParser()

        parser.add_argument('serviceKey', type=str)
        args = parser.parse_args()
        return {'status': 'success', 'serviceKey':args['serviceKey']}

api.add_resource(CreateUser, '/user')

if __name__ == '__main__':
    app.run(debug=True)