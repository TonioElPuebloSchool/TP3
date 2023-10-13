import streamlit as st
import requests
from html import unescape
import streamlit.components.v1 as components

# Your code for making requests should be defined in this function
def make_google_request():
    req = requests.get("https://analytics.google.com/analytics/web/#/p407510831/reports/intelligenthome")
    return req

# Create a Streamlit app
st.title("Request and Display HTML")

# Button to make a Google request
if st.button("Make Google Request"):
    req = make_google_request()
    st.text(f"Status Code: {req.status_code}")
    st.markdown(req.cookies._cookies)

# Button to display HTML content
if st.button("Display HTML"):
    if req:
        components.html(unescape(req.text))
