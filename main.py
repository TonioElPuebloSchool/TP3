from flask import Flask, request, render_template, redirect, jsonify
import requests
import streamlit as st
import argparse
from oauth2client import client, file, tools
import os

app = Flask(__name__)

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
    number_of_visitors = 10 #get_number_of_visitors()
    
    return render_template('home.html', log_text=log_text, number_of_visitors=number_of_visitors)

# add route to calculate number of visitors
@app.route('/refresh-visitors', methods=['GET'])
def refresh_visitors():
    
    starting_date = request.args.get('start_date')
    ending_date = request.args.get('end_date')

    property_id = "407510831"
    dimensions = ["sessionSource"]
    metrics = ["newUsers", "totalUsers"]

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'datasource.json'

    from google.analytics.data_v1beta import BetaAnalyticsDataClient
    from google.analytics.data_v1beta.types import (
        DateRange,
        Dimension,
        Metric,
        RunReportRequest,
    )
    client = BetaAnalyticsDataClient()

    request_api = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[
            Dimension(name=dim) for dim in dimensions
            ],
            metrics=[
                Metric(name=metr) for metr in metrics
            ],
            date_ranges=[DateRange(start_date=starting_date, end_date=ending_date)],
        )
    response = client.run_report(request_api)

    # retreive value of metric header totalUsers
    metric_header = [header.name for header in response.metric_headers]
    metrics = [0 for i in metric_header]
    for i in range(len(metric_header)):
        for row in response.rows :
            metrics[i]  += (int(row.metric_values[i].value))
    # now metrics[0] is new users and metrics[1] is total users
    print(metrics)
    return jsonify({
        "new_users": metrics[0],  # Update with the calculated new users count
        "total_users": metrics[1],  # Update with the calculated total users count
    })

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
    return redirect("http://localhost:8501")


if __name__ == '__main__':
    app.run(debug=True)
