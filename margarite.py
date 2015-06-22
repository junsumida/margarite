from facebookads.api import FacebookAdsApi
from facebookads import objects
import yaml, json
from datetime import date, timedelta
from collections import defaultdict

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

    if not install_count == 0:
        cpi = spend / install_count
    else:
        cpi = 0

    response = Response(json.dumps({"install_count":install_count, "spend":spend, "date":yesterday_date_string, "cpi":cpi}), mimetype='application/json')

    return response

@app.route("/last_week")
def report_of_last_week():
    me = objects.AdUser(fbid='me')
    my_accounts = list(me.get_ad_accounts())

    insights = my_accounts[1].get_report_stats(params={"date_preset":'last_week',"data_columns":["reach","spend","adgroup_id","account_name","clicks","actions"],"actions_group_by":["action_device","action_type"]})
    formatted_insights = defaultdict(lambda: [], {})
    for insight in insights:
        if insight["date_start"] == insight["date_stop"]:
            temp_insight = {
                "date": insight["date_start"],
                "reach": insight["spend"],
                "account_name": insight["account_name"],
                "spend": insight["spend"],
                "install": 0
            }
            if isinstance(insight["actions"], list) or isinstance(insight["actions"], dict):
                for action in insight["actions"]:
                    if action["action_type"] == "mobile_app_install":
                        temp_insight["install"] += action["value"]
            print temp_insight
            formatted_insights[insight["adgroup_id"]].append(temp_insight)
        else:
            print "invalid date"
            print insight
            continue

    for adgroup_id, insights_by_adg_id in formatted_insights.iteritems():
        formatted_insights[adgroup_id] = sorted(insights_by_adg_id, key=lambda i: i['date'])

    return Response(json.dumps(formatted_insights), mimetype='application/json')

def install_count_and_spend(insights):
    count = 0
    spend = 0

    for insight in insights:
        if not (isinstance(insight["actions"], list) or isinstance(insight["actions"], dict)):
            continue
        for action in insight["actions"]:
            if action["action_type"] == "mobile_app_install":
                count += action["value"]
        spend += insight["spend"]

    return count, spend

if __name__ == "__main__":
    app.debug = True
    app.run()
