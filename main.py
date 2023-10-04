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

    if request.method == 'POST':
        log_message = request.form['log_message']
        
        # Print the log message on the server-side (Python)
        app.logger.warning(f"Log message from Python: {log_message}")

        # Create JavaScript code to log a message on the browser's console
        log_browser = f'<script>console.log("Log message from browser: {log_message}");</script>'
        
        return log_browser
    
    
    # Render a simple HTML form to input the log message
    return "Voici un beau log !!"