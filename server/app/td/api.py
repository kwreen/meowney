import requests
import constants
import json


RESULT_KEY = "result"
CUSTOMERS_KEY = "customers"
CONTINUATION_TOKEN_KEY = "continuationToken"

API = "https://api.td-davinci.com/api"

def get_customer(custId: str):
    response = requests.get(
        API + '/customers/' + custId,
        headers = { 'Authorization': constants.TD_API_KEY })
    return response.json()

def get_customers():
    response = requests.post(
        API + '/raw-customer-data',
        headers = { 'Authorization': constants.TD_API_KEY })
    return response.json()

def get_customers_continued(continuationToken: str):
    response = requests.post(
        API + '/raw-customer-data',
        headers = { 'Authorization': constants.TD_API_KEY }, json = { "continuationToken": continuationToken})
    return response.json()

def get_transactions_by_cust_id(custId: str):
    response = requests.get(
        API + '/customers/' + custId + '/transactions',
        headers = { 'Authorization': constants.TD_API_KEY }
    )

    return response.json()