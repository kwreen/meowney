from app import state
from app.api import bp
from app.model import CategoryTag
from app.td import db
from app.util import transaction_helper
from flask import jsonify

@bp.route('/transaction/initialize', methods=['POST'])
def initialize_past_transactions_db():
    return db.initialize_past_transactions_db()
    
@bp.route('/transaction/relative', methods=['GET'])
def get_relative_transactions():
    total_transactions = {
        CategoryTag.SHOPPING: [],
        CategoryTag.FOOD_AND_DINING: [],
        CategoryTag.ENTERTAINMENT: []
    }

    print(state.similar_customers_cache)
    for customer in state.similar_customers_cache:
        customer_transactions = db.get_transactions_by_category_tag(customer['id'])
        total_transactions[CategoryTag.SHOPPING].extend(customer_transactions[CategoryTag.SHOPPING])
        total_transactions[CategoryTag.FOOD_AND_DINING].extend(customer_transactions[CategoryTag.FOOD_AND_DINING])
        total_transactions[CategoryTag.ENTERTAINMENT].extend(customer_transactions[CategoryTag.ENTERTAINMENT])

    state.relative_transactions_cache[CategoryTag.SHOPPING] = transaction_helper.groupByMonth(total_transactions[CategoryTag.SHOPPING])
    state.relative_transactions_cache[CategoryTag.FOOD_AND_DINING] = transaction_helper.groupByMonth(total_transactions[CategoryTag.FOOD_AND_DINING])
    state.relative_transactions_cache[CategoryTag.ENTERTAINMENT] = transaction_helper.groupByMonth(total_transactions[CategoryTag.ENTERTAINMENT])

    return jsonify(total_transactions)

@bp.route('/transaction/shopping/average', methods=['GET'])
def get_average_shopping_transactions():
    return _getAverageBy(CategoryTag.SHOPPING)

@bp.route('/transaction/food/average', methods=['GET'])
def get_average_food_transactions():
    return _getAverageBy(CategoryTag.FOOD_AND_DINING)

@bp.route('/transaction/entertainment/average', methods=['GET'])
def get_average_entertainment_transactions():
    return _getAverageBy(CategoryTag.ENTERTAINMENT)

def _getAverageBy(category: CategoryTag):
    result = {}
    if (not state.relative_transactions_cache[category]):
        get_relative_transactions()

    transaction_list = state.relative_transactions_cache[category]

    for item in transaction_list:
        try:
            result[item] = round(sum(transaction['currencyAmount'] for transaction in transaction_list[item]) / len(state.similar_customers_cache), 2)
        except ZeroDivisionError:
            result[item] = 0

    return result