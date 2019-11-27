import requests

from tenx.app import TenxApp

def slack(message):
    url = TenxApp.config.get('TENX_NOTIFICATIONS_SLACK')
    if not url: return
    response = requests.post(url, json={'text': message})
    if not response.ok: raise Exception("Slack POST failed for {}".format(url))

#-- slack
