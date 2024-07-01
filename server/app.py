#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
from models import db, Bakery, BakedGood
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')  # getting all the bakeries
def bakeries():
    bakeries = Bakery.query.all()

    # Create a list to store the JSON representations of bakery objects
    bakery_list = []

    for bakery in bakeries:
        bakery_dict = {
            'id': bakery.id,
            'name': bakery.name,
            'created_at': bakery.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': (bakery.updated_at.strftime('%Y-%m-%d %H:%M:%S') if bakery.updated_at else None),
        }
        bakery_list.append(bakery_dict)

    response = make_response(jsonify(bakery_list), 200)
    response.headers["Content-Type"] = "application/json"

    return response


@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter_by(id=id).first()

    if bakery is None:
        # Handle the case where the bakery with the specified ID is not found
        return jsonify({"error": "Bakery not found"}), 404

    bakery_dict = {
        'id': bakery.id,
        'name': bakery.name,
        'created_at': bakery.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'updated_at': (bakery.updated_at.strftime('%Y-%m-%d %H:%M:%S') if bakery.updated_at else None),
    }

    response = make_response(jsonify(bakery_dict), 200)
    response.headers['Content-Type'] = 'application/json'

    return response


@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    # Query baked goods and order them by price in descending order
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()

    baked_goods_list = [
        {
            'id': baked_good.id,
            'name': baked_good.name,
            'price': baked_good.price,
            'created_at': baked_good.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': (baked_good.updated_at.strftime('%Y-%m-%d %H:%M:%S') if baked_good.updated_at else None),
        }
        for baked_good in baked_goods
    ]
    response = make_response(jsonify(baked_goods_list), 200)
    response.headers['Content-Type'] = 'application/json'

    return response


@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    # Query the most expensive baked good by ordering in descending order and limiting to one result
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).first()

    if most_expensive is None:
        # Handle the case where there are no baked goods
        return jsonify({"error": "No baked goods found"}), 404

    # Serialize the most expensive baked good into JSON
    baked_good_dict = {
        'id': most_expensive.id,
        'name': most_expensive.name,
        'price': most_expensive.price,
        'created_at': most_expensive.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'updated_at': (most_expensive.updated_at.strftime('%Y-%m-%d %H:%M:%S') if most_expensive.updated_at else None),
    }

    response = make_response(jsonify(baked_good_dict), 200)
    response.headers['Content-Type'] = 'application/json'

    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
