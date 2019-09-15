import os
import sys
from app.model import CategoryTag
from app.td import api
from app.util import transaction_helper
from datetime import datetime
from tinydb import TinyDB, Query, where


Customers = TinyDB(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../customers.json'), default_table='Customers')
PastTransactions = TinyDB(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../pastTransactions.json'), default_table='PastTransactions')

AGE_OFFSET = 1
INCOME_OFFSET = 3000

def initialize_customers_db():
    BREAK_TOKEN = "1_1000"
    customer_list = []
    response = api.get_customers()


    while (response[api.RESULT_KEY][api.CONTINUATION_TOKEN_KEY]):
        continuationToken = response[api.RESULT_KEY][api.CONTINUATION_TOKEN_KEY]
        customer_list.extend(response[api.RESULT_KEY][api.CUSTOMERS_KEY])
        response = api.get_customers_continued(continuationToken)

        print(continuationToken)
        if (continuationToken == BREAK_TOKEN):
            break

    Customers.insert_multiple(customer_list)
    return customer_list

def initialize_past_transactions_db():
    past_transaction_list = []
    currentDateTime = datetime.now()

    for customer in Customers.all():
        response = api.get_transactions_by_cust_id(customer["id"])

        for transaction in response[api.RESULT_KEY]:
            transactionDateTime = transaction_helper.getDateTime(transaction['originationDateTime'])
            if (transactionDateTime < datetime.now()):
                past_transaction_list.append(transaction)

    PastTransactions.insert_multiple(past_transaction_list)

    return past_transaction_list

def get_customer(custId: str):
    return Customers.search(where('id') == custId)

def get_similar_customers(age: int, municipality: str, totalIncome: float):
    AGE_KEY = 'age'
    TOTAL_INCOME_KEY = 'totalIncome'

    customers = Customers.search(
        (where(AGE_KEY) <= age + AGE_OFFSET) & (where(AGE_KEY) >= age - AGE_OFFSET) &
         (Query().addresses.principalResidence.municipality.search(municipality)) &
         (where(TOTAL_INCOME_KEY) < totalIncome + INCOME_OFFSET) & (where(TOTAL_INCOME_KEY) > totalIncome - INCOME_OFFSET))
    print(customers)
    return customers

def get_transactions_by_cust_id(custId: str):
    return PastTransactions.search(where('customerId') == custId)

def get_transactions_by_category_tag(custId: str):
    required_transactions = {
        CategoryTag.SHOPPING: [],
        CategoryTag.FOOD_AND_DINING: [],
        CategoryTag.ENTERTAINMENT: []
    }

    all_transactions = PastTransactions.search((where('customerId') == custId))

    for transaction in all_transactions:
        categoryTags = transaction['categoryTags']
        if (CategoryTag.SHOPPING in categoryTags):
            required_transactions[CategoryTag.SHOPPING].append(transaction)
        elif (CategoryTag.FOOD_AND_DINING in categoryTags):
            required_transactions[CategoryTag.FOOD_AND_DINING].append(transaction)
        elif (CategoryTag.ENTERTAINMENT in categoryTags):
            required_transactions[CategoryTag.ENTERTAINMENT].append(transaction)

    return required_transactions
