from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from services.products_service import ProductService

product_blueprint = Blueprint('products', __name__)

@product_blueprint.route('/products', methods=['POST'])
def create_product():

    data = request.form
    name = data.get('name')
    description = data.get('description')

    if not name:
        return jsonify({'error': 'Name is required'}), 400
    
    ProductService.create_product(name, description)
    return redirect(url_for('products.index'))

@product_blueprint.route('/')
def index():
    return render_template('index.html')

from flask import Blueprint, request, jsonify
from models.products import db, Products

product_blueprint = Blueprint('products', __name__)

# Ruta para modificar una tarea
@product_blueprint.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    data = request.json
    product = Products.query.get(id)
    
    if not product:
        return jsonify({"message": "Product not found"}), 404
    
    # Actualizar los campos
    product.name = data.get('name', product.name)
    product.description = data.get('description', product.description)
    
    try:
        db.session.commit()
        return jsonify({"message": "Product updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error updating product", "error": str(e)}), 500
