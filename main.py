from flask import Flask, request, render_template, redirect
import requests
import streamlit as st
import argparse
from oauth2client import client, file, tools


app = Flask(__name__)


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


@app.route("/", methods=['GET', 'POST'])
def root():
    #log_text = ""
    #if request.method == 'POST':
    #    log_text = request.form.get('log')
    #    print(log_text)
    #return render_template('home.html', log_text=log_text)
    log_text = ""
    if request.method == 'POST':
        log_text = request.form.get('log')
        print(log_text)
    
    # Retrieve the number of visitors from Google Analytics
    number_of_visitors = response #get_number_of_visitors()
    
    return render_template('home.html', log_text=log_text, number_of_visitors=number_of_visitors)


@app.route("/logger", methods=['GET', 'POST'])
def logger():
    if request.method == 'POST':
        text = request.form.get('textarea')
        print(text)
        return render_template('logger.html', text=text)

    return render_template('logger.html', text="")

@app.route('/google-request', methods=['GET'])
def google_request():
    return """
    <a href="/"><button>Back to Home</button></a>
    <form method="GET" action="/perform-google-request">
        <input type="submit" value="Make Google Request">
    </form>
    """

@app.route('/perform-google-request', methods=['GET'])
def perform_google_request():
    req = requests.get("https://www.google.com")
    st.markdown(req.cookies._cookies)
    # st.markdown(req.cookies._cookies) doesn't seems to work
    # return f"Status Code for Google : {req.status_code}\nCookies: {req.cookies._cookies}"
    
    # we can also retunr for both google ang google analytics
    req2 = requests.get("https://analytics.google.com/analytics/web/#/p407510831/reports/intelligenthome")
    return f"Status Code for Google :\n {req.status_code}\n\nCookies: \n{req.cookies._cookies}\n\n\nStatus Code for Google Analytics : \n{req2.status_code}\n\nCookies: \n{req2.cookies._cookies}"

# to use streamlit app in flask
# it's running on port 8501 and seperate from flask app
@app.route("/streamlit")
def streamlit_link():
    # Redirect to the URL where you're running the Streamlit app
    return redirect("http://localhost:8501")  # Replace with the actual URL of your Streamlit app


if __name__ == '__main__':
    app.run(debug=True)
