from flask import Flask, request, render_template, redirect
import requests
import argparse
from oauth2client import client, file, tools


# we first need to ask for authentification to google analytics
credential_path = "client_secret.json"
refresh_token = "refresh_token.json"
scopes = ['https://www.googleapis.com/auth/analytics.readonly']

parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[tools.argparser])
flags = parser.parse_args([])
flow = client.flow_from_clientsecrets(
    credential_path, scope=scopes,
    message=tools.message_if_missing(credential_path))
storage = file.Storage(refresh_token)
credentials = storage.get()
if credentials is None or credentials.invalid:
    credentials = tools.run_flow(flow, storage, flags)

# now we need to generate a new access token
def generate_access_token(client_ID, client_secret, refresh_token, scopes, grant_type='refresh_token'):
    access_token = None
    api_endpoint = 'https://accounts.google.com/o/oauth2/token'
    scopes = 'https://www.googleapis.com/auth/analytics.readonly'
    
    url = f"{api_endpoint}?client_id={client_ID}&client_secret={client_secret}&refresh_token={refresh_token}&grant_type={grant_type}&scopes={scopes}"
    
    payload = {}
    headers = {}
    
    response = requests.request("POST", url, headers=headers, data=payload)
    
    if response.status_code == 200:
        access_token = response.json()['access_token']
        
    return access_token

# we can now make a request to google analytics
access_token = generate_access_token(client_ID=credentials.client_id, client_secret=credentials.client_secret, refresh_token=credentials.refresh_token, scopes=scopes)
property_id = "407510831"
start_date = "2023-01-01"
end_date = "2023-12-10"
iteration = 1
dimensions = ["dateHour", "sessionCampaignId", "sessionCampaignName", "sessionManuelTerm", "sessionMedium", "sessionSource", "pageReferrer"]
metrics = ["sessions", "newUsers", "totalUsers"]

def ga4_api_response(access_token, property_id, start_date, end_date, iteration, dimensions, metrics, limit=1000):
    url = f"https://analyticsreporting.googleapis.com/v1beta/{property_id}/batchRunReports"
    
    request_body = {
        "reportRequests": [
            {
                "viewId": f"{property_id}",
                "dateRanges": [
                    {
                        "startDate": f"{start_date}",
                        "endDate": f"{end_date}"
                    }
                ],
                "dimensions": [{"name": name} for name in dimensions],
                "metrics": [{"name": name} for name in metrics],
                "limit": limit,
                "offset": (iteration)*limit
            }
        ]
    }
    payload = f"""{request_body}"""
    headers = {
        'Content-Type': 'application/json',
        "Accept": "application/json",
        "Authorization": f"Bearer {str(access_token)}"
    }
    
    try:
        response = requests.request("POST", url, headers=headers, data=payload)
    except Exception as e:
        print(e)
        response = None
    
    return response

# we can now make a request to google analytics
response = ga4_api_response(access_token=access_token, property_id=property_id, start_date=start_date, end_date=end_date, iteration=iteration, dimensions=dimensions, metrics=metrics, limit=1000)
print(response)