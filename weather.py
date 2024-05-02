# Import Packages
import os
import logging
import csv
import datetime
import json
import time

import requests
from bs4 import BeautifulSoup

from funcs.smtp_gmail_func import *

# Enable Logging
script_name:str = "weather.py"
sys_datetime = datetime.datetime.now()
log_file:str = f"./logs/weather_{sys_datetime.strftime('%d%m%Y')}_{sys_datetime.hour}00.log"

logging.basicConfig(filename=log_file, filemode='w', level=logging.DEBUG, format='%(name)s - %(levelname)s - %(message)s')

# Sends a GET Request to WeatherAPI
# and returns the daily hourly forecast as list
def getRequest(base_url, latitude, longtitude) -> list:
    logging.info(f"Sending GET Request to WeatherAPI for ({latitude}, {longtitude})")
    url = f"{base_url}&q={latitude},{longtitude}"
    getRequest = requests.get(url)
    logging.info(f"Status Code [{getRequest.status_code}]")
    if (getRequest.status_code == 200):
        logging.info(f"Parsing Response")
        soup = BeautifulSoup(getRequest.text, "html.parser")
        response = soup.text
        hourly_forecast = json.loads(response)
        return hourly_forecast['forecast']['forecastday'][0]['hour']
    else:
        return([False])

# Retrieves the Weather Condition / Icon 
def getForecasts(loc_name, hourly_forecast) -> str:
    current_hour:int = datetime.datetime.now().hour

    html = f'<br/><table role="presentation" class="forecast" border="1" align="center" cellpadding="10px"><th colspan="3"><h2>{loc_name}</h2></th></tr><tr><th><h2>Hour</h2></th><th colspan="2"><h2>Weather</h2></th></tr>'
    
    for i in range(current_hour, 24):

        if (i < 10):
            hour = f"0{i}:00"
        else:
            hour = f"{i}:00"
        
        condition = hourly_forecast[i]['condition']['text']
        icon = hourly_forecast[i]['condition']['icon']

        html = html + f'<tr><td><p>{hour}</p></td><td><p>{condition}</p></td><td><img src="https:{icon}" alt="Icon for {condition}"/></td></tr>'
    
    html = html + f'</table>'
    return(html)

def main():
    try:
        os
        # Initialize Dependancy Variables
        key:str = os.environ.get("WEATHER_API_KEY")
        base_url:str = f"https://api.weatherapi.com/v1/forecast.json?key={key}"
        locationsCoordsFile:str = "./data/locations_latlong.csv"
        sys_datetime = datetime.datetime.now()
        subject:str = f"Weather Forecast ({sys_datetime.strftime('%d/%m/%y')}, {sys_datetime.hour}:00)"
        body_html:str = '<!DOCTYPE html><html><head><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&display=swap"><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style type="text/css">h1{font-size:56px}h2{font-size:28px;font-weight:900}h3{font-size:22px;font-weight:500}p{font-weight:300}td{vertical-align:center}#email{margin:auto;width:600px;background-color:#fff}.forecast{border-collapse:collapse;width:600px}</style></head><body bgcolor="#F5F8FA" style="width:100%;font-family:Roboto,sans-serif;font-size:18px"><div id="email"><table role="presentation" width="600px"><tr><td bgcolor="#00A4BD" align="center" style="color:#fff"><h1>Weather Forecast</h1></td></table><table role="presentation" border="0" cellpadding="0" cellspacing="10px" style="padding:30px 30px 30x 30px">'
        
        # Read Locations file:
        logging.info(f"Read Locations File [{locationsCoordsFile}] as List")
        with open(locationsCoordsFile, newline='') as f:
            reader = csv.reader(f)
            locations:list = list(reader)

            # Exit if no locations in file
            if (len(locations) <= 1):
                logging.info("No Locations, exiting with status 0")
                print("No Locations, exiting program.")
                return(0)
        
        # Process Each Location
        toSend = False
        for eachLocation in locations[1:]:
            if (len(eachLocation) == 3):
                logging.info(f"Processing Location: [{eachLocation}]")
                loc_name:str = eachLocation[0]
                latitude:float = eachLocation[1]
                longtitutde:float = eachLocation[2]
                
                # GET REQUEST
                hourly_forecast:list = getRequest(base_url, latitude, longtitutde)
                if (hourly_forecast[0] == [False]):
                    logging.warning(f"Failed GET Request, skipping record")
                    continue
                else:
                    # Create HTML Table for Hourly Forecasts
                    forecastHTML:str = getForecasts(loc_name, hourly_forecast)
                    logging.info(f"Create HTML Table:\n[{forecastHTML}]")
                    body_html = body_html + forecastHTML
                    toSend = True

                time.sleep(10)
            else:
                logging.warning(f"Invalid Location: [{eachLocation}], skipping record")
                print(f"Invalid location found. [{eachLocation}]")
                continue

        # Send Email
        if(toSend == True):
            body_html = body_html + '</table><tr colspan="3"><h3>Powered by <a href="https://www.weatherapi.com/" title="Free Weather API">WeatherAPI.com</a></h3><a href="https://www.weatherapi.com/" title="Free Weather API"><img src="https://cdn.weatherapi.com/v4/images/weatherapi_logo.png" alt="Weather data by WeatherAPI.com" border="0"></a></tr></div></body></html>'
            logging.info(f"SEND EMAIL: {subject}")
            logging.info(f"{body_html}")
            smtp_status = sendEmail(
                subject=subject,
                recipient_email="your_email@example.com",
                html_body=body_html
            )
            logging.info(f"SMTP STATUS: {smtp_status}")

    except Exception as e:
        logging.error(e)
        smtp_status = sendEmail(
            subject=f"[{script_name}] Failed {datetime.datetime.now()}",
            recipient_email="your_email@example.com",
            html_body=e
        )
        logging.error(f"SMTP STATUS: {smtp_status}")

if __name__ == "__main__":
    main()
