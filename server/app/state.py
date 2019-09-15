_current_customer = {
    'age': 0,
    'municipality': '',
    'totalIncome': 0
}

similar_customers_cache = []

def update_similar_customers_cache():
    from app.td import db
    global similar_customers_cache
    similar_customers_cache = db.get_similar_customers(age=_current_customer['age'], municipality=_current_customer['municipality'], totalIncome=_current_customer['totalIncome'])

def set_current_customer(data):
    _current_customer['age'] = data['age']
    _current_customer['municipality'] = data['municipality']
    _current_customer['totalIncome'] = data['totalIncome']
    update_similar_customers_cache()


from app.model import CategoryTag
relative_transactions_cache = {
    CategoryTag.SHOPPING: {},
    CategoryTag.FOOD_AND_DINING: {},
    CategoryTag.ENTERTAINMENT: {}
}