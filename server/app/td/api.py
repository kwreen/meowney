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

# def initializeCustomerDB():
#     BREAK_TOKEN = "1_1000"
#     response = getCustomers()

#     while (response[RESULT_KEY][CONTINUATION_TOKEN_KEY]):
#         continuationToken = response[RESULT_KEY][CONTINUATION_TOKEN_KEY]
#         customer_list.extend(response[RESULT_KEY][CUSTOMERS_KEY])
#         response = getCustomersContinued(continuationToken)

#         print(continuationToken)
#         if (continuationToken == BREAK_TOKEN):
#             break

#     db.Customers.insert_multiple(customer_list)
#     return customer_list

# def initializePastTransactionDB():
#     past_transaction_list = []
#     currentDateTime = datetime.now()

#     for customer in db.Customers.all():
#         response = getTransactionsByCustId(customer["id"])

#         for transaction in response[RESULT_KEY]:
#             transactionDateTime = dateTimeHelper.get(transaction['originationDateTime'])
#             if (transactionDateTime < datetime.now()):
#                 past_transaction_list.append(transaction)

#     db.PastTransactions.insert_multiple(past_transaction_list)

#     return past_transaction_list