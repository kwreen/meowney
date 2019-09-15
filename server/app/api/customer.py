from app import state
from app.api import bp
from app.td import api, db
from flask import request

@bp.route('/customer/initialize', methods=['POST'])
def initialize_customers_db():
    return db.initialize_customers_db()

@bp.route('/customer/<id>', methods=['GET'])
def get_customer(id):
    return api.get_customer(id)

@bp.route('/customer', methods=['POST'])
def set_customer():
    data = request.get_json() or {}
    state.set_current_customer(data)
    return state._current_customer

