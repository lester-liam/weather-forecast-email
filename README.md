# Weather Forecast Email
Sends you the daily hourly forecast via email

## Packages Required

Install with package manager [pip](https://pip.pypa.io/en/stable/) if you do not have the following packages: `requests` and `beautifulsoup4`.

```bash
pip install requests
pip install beautifulsoup4
```
## Prerequisites
### Weather Data | Powered by [WeatherAPI.com](https://www.weatherapi.com/)
Weather Information is retrieved via [WeatherAPI.com](https://www.weatherapi.com) using GET Requests. You'll need to sign-up for an account as you will need an access token to retrieve the weather conditions.

You can find out more about their API in their [docs](https://www.weatherapi.com/docs/)

### SMTP Credentials
Currently, the code is set to Google's SMTP Server. However if you're using other email providers, please change the server settings.
```python
smtp_server = 'smtp.gmail.com'
smtp_port = 465
```

### Before Running The Code
Set your environment variables

```python
# Environment Variables
WEATHER_API_KEY="YOUR_API_KEY"
SMTP_LOGIN_USERNAME="USERNAME"
SMTP_LOGIN_PASSWORD="PASSWORD"
```

Update your recipient/receiver address
```python
# Change to your email
recipient_email="your_email@example.com",
```

## License

[Unlicense](https://unlicense.org/)