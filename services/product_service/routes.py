
from flask import Blueprint, request, jsonify
from models import db, Product

product_bp = Blueprint('product_bp', __name__)

@product_bp.route('/', methods=['GET'])
def list_products():
    products = Product.query.all()
    return jsonify([p.to_dict() for p in products]), 200

@product_bp.route('/', methods=['POST'])
def add_product():
    data = request.get_json()
    if not (data and data.get("name") and data.get("price")):
        return jsonify({"message": "Missing product data"}), 400

    new_product = Product(name=data["name"], description=data.get("description", ""), price=data["price"])
    db.session.add(new_product)
    db.session.commit()
    return jsonify({"message": "Product added successfully", "product": new_product.to_dict()}), 201
