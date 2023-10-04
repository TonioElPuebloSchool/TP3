from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route("/")
def root():
    prefixe = """<!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-PVE1J5NDNL"></script>
    <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());

    gtag('config', 'G-PVE1J5NDNL');
    </script>"""
    return prefixe + "Hello from Space! 🚀"
# change

@app.route('/logger', methods=['GET', 'POST'])
def logger():
    print("logger  succeed")
    text_toshow = "logger succeed"