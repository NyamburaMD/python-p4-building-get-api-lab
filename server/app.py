#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    all_bakeries = Bakery.query.all()
    bakery_list = [{"id": b.id, "name": b.name, "created_at": b.created_at.isoformat() if b.created_at else None} for b in all_bakeries]
    return make_response(jsonify(bakery_list), 200)

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.get_or_404(id)
    if not bakery:
        return make_response(jsonify({'error': 'Bakery not found'}), 404)
    
    bakery_data = {
        "id": bakery.id,
        "name": bakery.name,
        "created_at": bakery.created_at.isoformat() if bakery.created_at else None,
        "baked_goods": [
            {
                "id": bg.id,
                "name": bg.name,
                "price": bg.price,
                "created_at": bg.created_at.isoformat() if bg.created_at else None,
                "bakery_id": bg.bakery_id,
            } for bg in bakery.baked_goods
        ]
    }
    return make_response(jsonify(bakery_data), 200)

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_serialized = [
        {
            "id": bg.id,
            "name": bg.name,
            "price": bg.price,
            "created_at": bg.created_at.isoformat() if bg.created_at else None,
            "bakery_id": bg.bakery_id,
        } for bg in baked_goods
    ]
    return make_response(jsonify(baked_goods_serialized), 200)

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    baked_good = BakedGood.query.order_by(BakedGood.price.desc()).first()
    if not baked_good:
        return jsonify({"error": "No baked goods found"}), 404

    baked_good_serialized = {
        "id": baked_good.id,
        "name": baked_good.name,
        "price": baked_good.price,
        "created_at": baked_good.created_at.isoformat() if baked_good.created_at else None,
        "bakery_id": baked_good.bakery_id
    }
    return jsonify(baked_good_serialized), 200
    


if __name__ == '__main__':
    app.run(port=5555, debug=True)
