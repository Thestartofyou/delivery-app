from flask import Flask, request
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

orders = []
order_id_counter = 1

class OrderResource(Resource):
    def get(self, order_id=None):
        if order_id:
            order = next((o for o in orders if o['id'] == order_id), None)
            if order:
                return {'order': order}
            return {'message': 'Order not found'}, 404
        return {'orders': orders}

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('customer_name', type=str, required=True, help='Customer name is required')
        parser.add_argument('delivery_address', type=str, required=True, help='Delivery address is required')
        parser.add_argument('items', type=list, required=True, help='Items list is required')
        args = parser.parse_args()

        order = {
            'id': order_id_counter,
            'customer_name': args['customer_name'],
            'delivery_address': args['delivery_address'],
            'items': args['items'],
            'status': 'Pending'
        }

        orders.append(order)
        global order_id_counter
        order_id_counter += 1

        return {'message': 'Order placed successfully', 'order': order}, 201

    def put(self, order_id):
        order = next((o for o in orders if o['id'] == order_id), None)
        if not order:
            return {'message': 'Order not found'}, 404

        parser = reqparse.RequestParser()
        parser.add_argument('status', type=str, required=True, help='Status is required')
        args = parser.parse_args()

        order['status'] = args['status']

        return {'message': 'Order status updated successfully', 'order': order}

    def delete(self, order_id):
        global orders
        orders = [o for o in orders if o['id'] != order_id]
        return {'message': 'Order deleted successfully'}

api.add_resource(OrderResource, '/orders', '/orders/<int:order_id>')

if __name__ == '__main__':
    app.run(debug=True)
