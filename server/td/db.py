import os
import sys
from tinydb import TinyDB, Query, where


Customers = TinyDB(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../customers.json'), default_table='Customers')
PastTransactions = TinyDB(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../pastTransactions.json'), default_table='PastTransactions')

AGE_OFFSET = 1
INCOME_OFFSET = 3000

def test():
    return "test"

def getCustomer(custId: str):
    return Customers.search(where('id') == custId)

def getSimilarCustomers(age: int, municipality: str, totalIncome: float):
    customers = Customers.search(
        (where('age') <= age + AGE_OFFSET) & (where('age') >= age - AGE_OFFSET) &
         (Query().addresses.principalResidence.municipality.search(municipality)) &
         (where('totalIncome') < totalIncome + INCOME_OFFSET) & (where('totalIncome') > totalIncome - INCOME_OFFSET))
    print(customers)
    return customers

def getTransactionsByCustId(custId: str):
    return PastTransactions.search(where('customerId') == custId)

def getTransactionsByCategoryTag(custId: str):
    SHOPPING = "Shopping"
    FOOD_AND_DINING = "Food and Dining"
    ENTERTAINMENT = "Entertainment"

    required_transactions = {
        SHOPPING: [],
        FOOD_AND_DINING: [],
        ENTERTAINMENT: []
    }

    all_transactions = PastTransactions.search((where('customerId') == custId))

    for transaction in all_transactions:
        categoryTags = transaction['categoryTags']
        if (SHOPPING in categoryTags):
            required_transactions[SHOPPING].append(transaction)
        elif (FOOD_AND_DINING in categoryTags):
            required_transactions[FOOD_AND_DINING].append(transaction)
        elif (ENTERTAINMENT in categoryTags):
            required_transactions[ENTERTAINMENT].append(transaction)

    return required_transactions
