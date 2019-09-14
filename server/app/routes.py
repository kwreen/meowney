from app import app
from td import tdApi
import json

@app.route('/')
def get():
    return json.dumps(tdApi.initializeCustomerData())
