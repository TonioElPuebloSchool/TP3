<img style="float: left; padding-right: 10px; width: 200px" src="https://upload.wikimedia.org/wikipedia/fr/b/b1/Logo_EPF.png?raw=true"> 

## Data Sources
**P2024** antoine-courbi

# Digital traces TP2

### Created by Antoine Courbi
-----
### [*Moodle course*](https://moodle.epf.fr/course/view.php?id=9502&section=1)
### [*Github depository*](https://github.com/TonioElPuebloSchool/TP1)
-----

This **README** is meant to explain `how the app works` and what was done during the `TP`.

# **Useful links**
The web page is accessible here : https://tp2deta-1-r1097488.deta.app/  
Deta dashboard is accessible here (that’s for me) : https://deta.space/  
Google analytics is accessible here (again for me) : https://analytics.google.com/analytics/web/#/p407510831/realtime/overview?params=_u..nav%3Dmaui  
The public git project repository is accessible here : https://github.com/TonioElPuebloSchool/TP2  
Console google API (for me) : https://console.cloud.google.com/apis/dashboard?project=datasource-401916

# **What we did**
We used python and Flask to display log on python and on the browser (visible from the detalog and from the console of the browser running the webpage). We printed a message in a textbox as well.
We used requests to manipulate cookies on google and on our ganalytics to display them. We tried to use streamlit to display the cookies.
Finally, we used oauth2client to display specific cookies about our webpage (ganalytics views).


# **How to run the app**
The app is running on https://tp2deta-1-r1097488.deta.app/.  
You can enter a message and submit it and it will appear on the console log of the browser, on the deta log and on the webpage.  
You can also select a start date and an end date and submit it to display the cookies of the google analytics of the webpage, specifically the views (newUsers and totalUsers).

# **Explaination of the code**
## Application Overview
The application looks like this :  
<img style="float: center; width: 300px" src="images\application_overview.png">
## Extended explanations
Concerning logger, it was in the /logger route at the beginning but in the end I also display loggers in the main page as it’s where I show everything. In itself its pretty simple, I have this in the home route:
```python
log_text = ""
    if request.method == 'POST':
        log_text = request.form.get('log')
        print(log_text)
```

And this to display the log on the webpage:
```html
<script>
        console.log("{{ log_text }}");
</script>
```

Hence when I enter a log it shows it on the app and on the browser (locally since Deta wasn’t working but it works the same):  
<img style="float: center; width: 800px" src="images\log.png">  

Concerning cookies, its pretty straigforward.  
We can also use streamlit by running it in another terminal : 
```bash
PS C:\Users\antoi\OneDrive\Documents\COURS_2023_S2\Data_Sources\TP2> streamlit run streamlit_app.py
>> 

  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.1.17:8501
```
Now we can see this :  
<img style="float: center; width: 500px" src="images\streamlit.png">  

So it works great, but I didn’t want to implement that on the main page as its not really interesting. The interesting part is to retrieve information from the cookies.
Concerning oauth, I tried different things to make the user log into google to have permissions using this :
```python
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
```
And it works, except its not necessary as we can access the cookies of our analytic by login in using credentials of my “compte de service” key. We can use this “compte de service” and attribute the administration access on google console.
In the end in my main page I have a button that redirect to a route that make the google request and calculate the number of new users and total users depending on the response using this code :
```python
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
```
Then I simply display it in my home page :

<img style="float: center; width: 400px" src="images\number_visitors_1.png">  

I can change the dates to specify my request :  

<img style="float: center; width: 400px" src="images\number_visitors_2.png">  



Thanks for reading this far !
Have a great day !