from facebookads.api import FacebookAdsApi
from facebookads import objects
import yaml
import json

from flask import Flask, jsonify, abort, Response
app = Flask(__name__)

settings_file = open('margarite.yml').read()
settings      = yaml.load(settings_file)

my_app_id       = settings['app_id'] 
my_app_secret   = settings['app_secret']
my_access_token = settings['access_token']
FacebookAdsApi.init(my_app_id, my_app_secret, my_access_token)

@app.route("/")
def ad_accounts():
    me = objects.AdUser(fbid='me')
    my_accounts = list(me.get_ad_accounts())
    accounts = map(lambda ad_account: ad_account['id'], my_accounts)
    response = Response(json.dumps(accounts), mimetype='application/json')

    return response

if __name__ == "__main__":
    app.debug = True
    app.run()
