import requests
import constants
import json
import os
import sys

from tinydb import TinyDB, Query

customer_list = []

RESULT_KEY = "result"
CUSTOMERS_KEY = "customers"
CONTINUATION_TOKEN_KEY = "continuationToken"

def getCustomerData():
    response = requests.post(
        'https://api.td-davinci.com/api/raw-customer-data',
        headers = { 'Authorization': constants.TD_API_KEY })
    return response.json()

def getCustomerDataContinued(continuationToken):
    response = requests.post(
        'https://api.td-davinci.com/api/raw-customer-data',
        headers = { 'Authorization': constants.TD_API_KEY }, json = { "continuationToken": continuationToken})
    return response.json()

def initializeCustomerData():
    response = getCustomerData()

    while (response[RESULT_KEY][CONTINUATION_TOKEN_KEY]):
        continuationToken = response[RESULT_KEY][CONTINUATION_TOKEN_KEY]
        customer_list.extend(response[RESULT_KEY][CUSTOMERS_KEY])
        response = getCustomerDataContinued(continuationToken)

        print(continuationToken)
        if (continuationToken == "10_1000"):
            break

    print(customer_list[0])
    db = TinyDB(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../customers.json'))
    db.insert_multiple(customer_list)
    return customer_list

    