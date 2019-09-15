from datetime import datetime


def get(datetimeStr: str):
    transactionDateTime = None
    try:
        transactionDateTime = datetime.strptime(datetimeStr, '%Y-%m-%dT%H:%M:%SZ')
    except ValueError:
        transactionDateTime = datetime.strptime(datetimeStr, '%Y-%m-%dT%H:%M:%S.%fZ')

    return transactionDateTime