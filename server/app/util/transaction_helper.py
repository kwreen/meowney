from datetime import datetime


def getDateTime(datetimeStr: str):
    transactionDateTime = None
    try:
        transactionDateTime = datetime.strptime(datetimeStr, '%Y-%m-%dT%H:%M:%SZ')
    except ValueError:
        transactionDateTime = datetime.strptime(datetimeStr, '%Y-%m-%dT%H:%M:%S.%fZ')

    return transactionDateTime

def groupByMonth(list: []):
    monthifiedLists = { 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: [], 11: [], 12: [] }

    for item in list:
        itemDateTime = getDateTime(item['originationDateTime'])
        monthifiedLists[itemDateTime.month].append(item)

    return monthifiedLists