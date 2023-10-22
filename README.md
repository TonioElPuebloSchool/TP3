<img style="float: left; padding-right: 10px; width: 200px" src="https://upload.wikimedia.org/wikipedia/fr/b/b1/Logo_EPF.png?raw=true"> 

## Data Sources
**P2024** antoine-courbi

# Digital traces TP3

### Created by Antoine Courbi
-----
### [*Moodle course*](https://moodle.epf.fr/course/view.php?id=9502&section=1)
### [*Github depository*](https://github.com/TonioElPuebloSchool/TP1)
### [*PDF TP*]()
-----

This **README** is meant to explain `how the app works` and what was done during the `TP`.

# **Useful links**
The web page is accessible here : https://tp3deta-1-q0219281.deta.app/  
Deta dashboard is accessible here (that’s for me) : https://deta.space/  
Google analytics is accessible here (again for me) : https://analytics.google.com/analytics/web/#/p407510831/realtime/overview?params=_u..nav%3Dmaui  
The public git project repository is accessible here : https://github.com/TonioElPuebloSchool/TP3  
Console google API (for me) : https://console.cloud.google.com/apis/dashboard?project=datasource-401916


# **What we did**
We learned what GDPR was, how it has evolved and what changed with it apparition.
We developed a new route in the web app to display google trend graphics using pytrends (generate data like google trend) and ChartJS (display a chart in a flask application).
We learned what a decorator was, we implement one that logs the execution time of a function. We used it to compare two occurrence methods and performed statistics on the results.

# **Ressources**
GDPR website : https://gdpr-info.eu/art-1-gdpr/  
Pytrends github doc : https://github.com/GeneralMills/pytrends  
Pytrends example : https://medium.com/@sinabaghaee96/data-extraction-from-google-trends-with-pytrends-1a89e33412bb  
ChartJS useful example : https://www.geeksforgeeks.org/how-to-add-graphs-to-flask-apps/  
Decorator information : https://www.datacamp.com/tutorial/decorators-python


# **How to run the app**
The app is running on https://tp3deta-1-q0219281.deta.app/.  
You can enter a message and submit it and it will appear on the console log of the browser, on the deta log and on the webpage.  
You can also select a start date and an end date and submit it to display the cookies of the google analytics of the webpage, specifically the views (newUsers and totalUsers).  
You can also click on the google trend botton at the bottom of the page that redirect to the google-trend route in which you can select a keyword and a start date to display a chart of the google trend of the keyword over time.


# **GDPR**

- ***What is it?***  
GDPR means General Data Protection Regulation and the objective of this regulation is to lays down rules that relates with the data protection of people, concerning both the processing and the movement of the data (https://gdpr-info.eu/art-1-gdpr/)
- **When has it been created and what was in place before?**
Before, each country had its own data protection rules and there was no common agreement at the country scale to protect individual. GDPR appeared in 2018.
- **What has it changed and why?**  
GDPR changed everything by creating a general regulation at the EU scale. So now people have moire control over their data, they can discard from companies. Also companies have to handle data more carefully now. For example now for most of website we can accept or decline cookies.

# **Google Trend**

I added a new route in main named google-trend to perform the request and display the chart.  
It looks like this :  
<img style="float: center; width: 400px" src="images\ggtrend01.png">  

By changing the keywords and changing the timeframe we can display another graph :  
<img style="float: center; width: 400px" src="images\ggtrend02.png">  

Important to note that timeframe is the starting date of the acquisition and should respect this format :  
* `timeframe`

  - Date to start from
  - Defaults to last 5yrs, `'today 5-y'`.
  - Everything `'all'`
  - Specific dates, 'YYYY-MM-DD YYYY-MM-DD' example `'2016-12-14 2017-01-25'`
  - Specific datetimes, 'YYYY-MM-DDTHH YYYY-MM-DDTHH' example `'2017-02-06T10 2017-02-12T07'`
      - Note Time component is based off UTC

  - Current Time Minus Time Pattern:

    - By Month: ```'today #-m'``` where # is the number of months from that date to pull data for
      - For example: ``'today 3-m'`` would get data from today to 3months ago
      - **NOTE** Google uses UTC date as *'today'*
      - **Works for 1, 3, 12 months only!**

    - Daily: ```'now #-d'``` where # is the number of days from that date to pull data for
      - For example: ``'now 7-d'`` would get data from the last week
      - **Works for 1, 7 days only!**

    - Hourly: ```'now #-H'``` where # is the number of hours from that date to pull data for
      - For example: ``'now 1-H'`` would get data from the last hour
      - **Works for 1, 4 hours only!**







Thanks for reading this far !
Have a great day !