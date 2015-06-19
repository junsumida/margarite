from facebookads.api import FacebookAdsApi
from facebookads import objects
import yaml, json
from datetime import date, timedelta

from flask import Flask, jsonify, abort, Response
app = Flask(__name__)

settings_file = open('margarite.yml').read()
settings      = yaml.load(settings_file)

my_app_id       = settings['app_id']
my_app_secret   = settings['app_secret']
my_access_token = settings['access_token']
FacebookAdsApi.init(my_app_id, my_app_secret, my_access_token)

@app.route("/yesterday")
def report_of_yesterday():
    me = objects.AdUser(fbid='me')
    my_accounts = list(me.get_ad_accounts())

    yesterday_date_string = (date.today() - timedelta(days=1)).isoformat()

    insights = my_accounts[1].get_report_stats(params={"date_preset":'yesterday',"data_columns":["reach","spend","adgroup_id","account_name","clicks","actions"],"actions_group_by":["action_device","action_type"]})
    print insights

    install_count, spend = install_count_and_spend(insights)

    cpi = spend / install_count

    response = Response(json.dumps({"install_count":install_count, "spend":spend, "date":yesterday_date_string, "cpi":cpi}), mimetype='application/json')

    return response

def install_count_and_spend(insights):
    count = 0
    spend = 0

    for insight in insights:
        for action in insight["actions"]:
            if action["action_type"] == "mobile_app_install":
                count += action["value"]
        spend += insight["spend"]

    return count, spend

if __name__ == "__main__":
    app.debug = True
    app.run()
