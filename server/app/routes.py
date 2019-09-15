from app import app
from td import api
from td import db
from datetime import datetime
from util import dateTimeHelper
import json

@app.route('/customers')
def getCustomers():
    return json.dumps(api.initializeCustomerDB())

@app.route('/transactions')
def getPasTransactions():
    return json.dumps(api.initializePastTransactionDB())

SHOPPING = "Shopping"
FOOD_AND_DINING = "Food and Dining"
ENTERTAINMENT = "Entertainment"

average_transactions_cache = {
    SHOPPING: {},
    FOOD_AND_DINING: {},
    ENTERTAINMENT: {}
}

customers = db.getSimilarCustomers(age=23, municipality='North York', totalIncome=12000) # todo

def getTransactionsFor(activity: str):
    if (not average_transactions_cache[activity]):
        getRelativeTransactions()

    return average_transactions_cache[activity]

@app.route('/average/shopping')
def getShoppingAverage():
    result = {}
    transactionList = getTransactionsFor(SHOPPING)

    for item in transactionList:
        try:
            result[item] = round(sum(transaction['currencyAmount'] for transaction in transactionList[item]) / len(customers), 2)
        except ZeroDivisionError:
            result[item] = 0

    return result

@app.route('/average/food')
def getFoodAverage():
    result = {}
    transactionList = getTransactionsFor(FOOD_AND_DINING)

    for item in transactionList:
        try:
            result[item] = round(sum(transaction['currencyAmount'] for transaction in transactionList[item]) / len(customers), 2)
        except ZeroDivisionError:
            result[item] = 0

    return result

@app.route('/average/entertainment')
def getEntertainmentAverage():
    result = {}
    transactionList = getTransactionsFor(ENTERTAINMENT)

    for item in transactionList:
        try:
            result[item] = round(sum(transaction['currencyAmount'] for transaction in transactionList[item]) / len(customers), 2)
        except ZeroDivisionError:
            result[item] = 0

    return result

@app.route('/test')
def getRelativeTransactions():
    total_transactions = {
        SHOPPING: [],
        FOOD_AND_DINING: [],
        ENTERTAINMENT: []
    }

    for customer in customers:
        customer_transactions = db.getTransactionsByCategoryTag(customer['id'])
        total_transactions[SHOPPING].extend(customer_transactions[SHOPPING])
        total_transactions[FOOD_AND_DINING].extend(customer_transactions[FOOD_AND_DINING])
        total_transactions[ENTERTAINMENT].extend(customer_transactions[ENTERTAINMENT])

    average_transactions_cache[SHOPPING] = groupByMonth(total_transactions[SHOPPING])
    average_transactions_cache[FOOD_AND_DINING] = groupByMonth(total_transactions[FOOD_AND_DINING])
    average_transactions_cache[ENTERTAINMENT] = groupByMonth(total_transactions[ENTERTAINMENT])

    return json.dumps(total_transactions)

def groupByMonth(list: []):
    monthifiedLists = { 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: [], 11: [], 12: [] }

    for item in list:
        itemDateTime = dateTimeHelper.get(item['originationDateTime'])
        monthifiedLists[itemDateTime.month].append(item)

    return monthifiedLists
