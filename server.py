from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
import sqlcipher3
from plaid.api import plaid_api
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid import Configuration, ApiClient
from flask import send_from_directory
import pickle

load_dotenv()

access_token_database_path = os.getenv("ACCESSTOKEN_DB")
access_token_database_key = os.getenv("DB_KEY")

app = Flask(__name__)

# --- Plaid API client configuration ---
configuration = Configuration(
    host="https://production.plaid.com",  # change to development/production when ready
    api_key={
        "clientId": os.getenv("PLAID_CLIENT_ID"),
        "secret": os.getenv("PLAID_SECRET")
    }
)

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

api_client = ApiClient(configuration)
client = plaid_api.PlaidApi(api_client)

# --- Routes ---
@app.route('/link/token/create', methods=['POST'])
def create_link_token():
    user=LinkTokenCreateRequestUser(client_user_id='user-123')
    try:
        request_data = LinkTokenCreateRequest(
            user=user,  # Must be exactly this key
            client_name="My Python App",
            products=[Products("auth"), Products("transactions")],
            country_codes=[CountryCode("US")],
            language="en"
        )
        response = client.link_token_create(request_data)
        print("Link token created:", response.to_dict())
        return jsonify(response.to_dict())
    except Exception as e:
        print("Error creating link token:", e)
        return jsonify({"error": str(e)}), 500

@app.route('/item/public_token/exchange', methods=['POST'])
def exchange_public_token():
    db = sqlcipher3.connect('secure.db')
    tablequery= """
    CREATE TABLE IF NOT EXISTS tokens (
            institution TEXT UNIQUE,
            token TEXT
            );
    """
    data = request.get_json()
    public_token = data.get('public_token')
    
    try:
        request_data = ItemPublicTokenExchangeRequest(public_token=public_token)
        exchange_response = client.item_public_token_exchange(request_data)
        access_token = exchange_response.to_dict()['access_token']
        data = exchange_response.to_dict()
        with open("data.pkl", 'wb') as f:
            pickle.dump(data, f)

        """db.execute(f"PRAGMA key={access_token_database_key}")
        #db.execute(tablequery)
        db.execute("INSERT INTO tokens (institution, token) VALUES (?, ?)", (institution, access_token))"""
        return jsonify({'access_token': access_token})

    except Exception as e:
        print(f"Error while creating access token: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(port=5000, debug=True)
