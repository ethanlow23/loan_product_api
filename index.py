from pymongo import MongoClient
import requests

client = MongoClient('mongodb://localhost:27017/')
db = client['loan_product']
users = db['users']
nodes = db['nodes']
loans = db['loans']
trans = db['trans']

client_keys = "client_id_gp2EIaZGVQXhJwz0viDbju4mFL1koONH8l9yS03Y|client_secret_epOgzf0FEkcnwU17yhqd8lDxjZoJY63HaAtRLSmQ"
endpoint = "https://uat-api.synapsefi.com/v3.1"
headers = {
    "X-SP-GATEWAY": client_keys,
    "X-SP-USER-IP": "127.0.0.1",
    "X-SP-USER": "|",
    "Content-Type": "application/json"
}

# USER/KYC FUNCTIONS

def get_users():
    resp = requests.get(endpoint + '/users', headers=headers)
    return resp

def create_user(data):
    resp = requests.post(endpoint + '/users', headers=headers, data=data)
    if resp.status_code == 200:
        users.insertOne(resp.json())
    return resp

def oauth_user(user_id):
    data = {
        "refresh_token": view_user(user_id).json()['refresh_token']
    }
    resp = requests.post(endpoint + '/oauth/' + user_id, headers=headers, data=data)
    return resp

def view_user(user_id):
    resp = requests.get(endpoint + '/users/' + user_id, headers=headers)
    return resp

def update_user(user_id, data):
    resp = requests.post(endpoint + '/users/' + user_id, headers=headers, data=data)
    if resp.status_code == 200:
        users.updateOne(user_id, { $push: resp.json() })
    return resp

# ACH FUNCTIONS

def link_bank_login(user_id, data):
    resp = requests.post(endpoint + '/users/' + user_id + '/nodes', headers=headers, data=data)
    if resp.status_code == 200:
        nodes.insertOne(resp.json())
    return resp

def link_account(user_id, data):
    resp = requests.post(endpoint + '/users/' + user_id + '/nodes', headers=headers, data=data)
    if resp.status_code == 200:
        nodes.insertOne(resp.json())
    return resp

def view_account(user_id, node_id):
    return requests.get(endpoint + '/users/' + user_id + '/nodes/' + node_id, headers=headers)

# LOANS FUNCTIONS

def preview_loan(user_id, data):
    return requests.post(endpoint + '/users/' + user_id + '/nodes', headers=headers, data=data)

def create_loan(user_id, data):
    resp = requests.post(endpoint + '/users/' + user_id + '/nodes', headers=headers, data=data)
    if resp.status_code == 200:
        loans.insertOne(resp.json())
    return resp

def view_loan(user_id, node_id):
    resp = requests.get(endpoint + '/users/' + user_id + '/nodes/' + node_id, headers=headers)
    return resp

def make_loan_payment(user_id, node_id, data):
    resp = requests.post(endpoint + '/users/' + user_id + '/nodes/' + node_id + '/trans', headers=headers, data=data)
    if resp.status_code == 200:
        trans.insertOne(resp.json())
    return resp

def view_loan_payment(user_id, node_id, trans_id):
    resp = requests.get(endpoint + '/users/' + user_id + '/nodes/' + node_id + '/trans/' + trans_id)
    return resp

def change_payment_date(user_id, node_id, data):
    return requests.post(endpoint + '/users/' + user_id + '/nodes' + node_id, headers=headers, data=data)

def change_payment_node(user_id, node_id, data):
    return requests.post(endpoint + '/users/' + user_id + '/nodes' + node_id, headers=headers, data=data)
