
# Day 35 - Weather Alert

A Python project that checks the OpenWeatherMap forecast
for the next 12 hours and identifies possible rain.

## Features
- Fetches weather forecast data using an API
- Checks rain probability and weather conditions
- Can send SMS alerts through Twilio
- Keeps API credentials in environment variables

## Setup
1. Install dependencies with `python -m pip install -r requirements.txt`
2. Set the OPENWEATHER_API_KEY environment variable.
3. Optionally configure Twilio environment variables.
4. Run `python main.py`.

Never commit API keys, authentication tokens, or private credentials.