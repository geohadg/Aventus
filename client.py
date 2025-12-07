key = '2feddaff8390028574ae122526aa23'
id = '68ed2d2c008bc30020882757'

import os
import plaid
from plaid.api import plaid_api

os.environ['plaidapiclientid'] = id
os.environ['plaidapiclientsecret'] = key

key = os.getenv('plaidapiclientsecret')
id = os.getenv('plaidapiclientid')

# Configure Plaid API client
configuration = plaid.Configuration(
    host=plaid.Environment.Production,  # Or plaid.Environment.Development, plaid.Environment.Production
    api_key={
        'clientId': id,
        'secret': key,
    }
)

api_client = plaid.ApiClient(configuration)
client = plaid_api.PlaidApi(api_client)
