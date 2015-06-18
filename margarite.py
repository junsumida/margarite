from facebookads.api import FacebookAdsApi
from facebookads import objects
import yaml

settings_file = open('margarite.yml').read()
settings      = yaml.load(settings_file)

my_app_id       = settings['app_id'] 
my_app_secret   = settings['app_secret']
my_access_token = settings['access_token']
FacebookAdsApi.init(my_app_id, my_app_secret, my_access_token)
