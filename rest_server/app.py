import os
import pickle

from flask import Flask, request
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

PICKLE = 'orders.pkl'
DRESPONSE = {
  'fulfillmentText': '',
}

if os.path.exists(PICKLE):
    with open(PICKLE, 'rb') as f:
        orders = pickle.load(f)
else:
    orders = dict()


class ClientInfo(Resource):
    def post(self):
        headers = request.headers
        data = request.get_json()
        #print(headers)
        ide = headers['Service']
        #print(data)
        paras = data['queryResult']['outputContexts'][-1]['parameters']
        customer = paras['customer']
        try:
            action = data['queryResult']['intent']['endInteraction']
        except KeyError:
            action = False
        print('here', action)
        if action:
            para_dict = orders.get(ide, dict())
            para_dict[customer] = paras
            orders[ide] = para_dict
            print(orders)
            res = DRESPONSE
            res['fulfilmentText'] = '{\'Archive\': \'Ok\'}'
            with open(PICKLE, 'wb') as f:
                pickle.dump(orders, f)
        else:
            res = DRESPONSE
            #res['fulfillmentText'] = '아래 정보로 주문을 완료하였습니다.\n{0}'.format(orders[ide][customer])
            res['fulfillmentText'] = '아래 정보로 주문을 완료하였습니다.'
            for key in orders[ide][customer].keys():
                if not key.endswith('.original'):
                    res['fulfillmentText'] = '{0}\n{1}: {2}'.format(res['fulfillmentText'],
                                                                    key,
                                                                    orders[ide][customer][key])
            res['fulfillmentText'] = res['fulfillmentText'].replace('"', '\'')
            res['outputContexts'] = [dict()]
            res['outputContexts'][0]['name'] = data['queryResult']['outputContexts'][0]['name']
            print(res)
        return res

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/')
api.add_resource(ClientInfo, '/clientinfo')

if __name__ == '__main__':
    app.run(debug=True)
