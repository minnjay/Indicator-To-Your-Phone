import datetime
from twilio.rest import Client
import quandl
# /usr/bin/env python
# Download the twilio-python library from twilio.com/docs/libraries/python
import os
import requests
import pandas as pd

url = "https://fear-and-greed-index.p.rapidapi.com/v1/fgi"

headers = {
    'x-rapidapi-key': "b6680da2a4msh1cc45ee54b45f32p1a6d0cjsnd22b8b7cba61",
    'x-rapidapi-host': "fear-and-greed-index.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers)

json_object = response.json()
value = json_object['fgi']['now']['value']
state = json_object['fgi']['now']['valueText']

cryptourl = 'https://api.alternative.me/fng/'
res = requests.request("GET", cryptourl)
c_json_object = res.json()
c_value = c_json_object['data'][0]['value']
c_state = c_json_object['data'][0]['value_classification']
ts = c_json_object['data'][0]['timestamp']

if(c_state == 'Extreme Greed'):
    c_state = 'E Greed'
elif(c_state == 'Extreme Fear'):
    c_state = 'E Fear'

treasuryYield = quandl.get("USTREASURY/YIELD", rows=1, authtoken="HB9yt-8sug3P5vXL-Xxf")
TYData = treasuryYield.values[-1]

TY3month = TYData[2]
TY10year = TYData[9]
diff_10year_3month = TY10year - TY3month

timestamp = datetime.datetime.fromtimestamp(int(ts))
line = 'FearG I\n{}\nEquity: {} [{}]\nCrypto: {} [{}]\nTBond-3mth: {}\nTBond-10yrs: {}\n10yrs-3mth: {}'.format(
    timestamp.strftime('%Y-%m-%d'), value, state, c_value, c_state, TY3month, TY10year, diff_10year_3month)


# Find these values at https://twilio.com/user/account
# To set up environmental variables, see http://twil.io/secure
account_sid = '' # your acc id from twilio
auth_token = '' # your auth token twilio

client = Client(account_sid, auth_token)

message = client.api.account.messages.create(
    to='', # phone number
    from_='', # phone number
    body=line)

# print(type(int(ts)))
# timestamp = datetime.datetime.fromtimestamp(int(ts))
# print(timestamp.strftime('%Y-%m-%d %H:%M:%S'))


