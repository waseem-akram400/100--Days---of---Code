# Day 66 - Cafe REST API

A beginner REST API built with Flask and CSV storage.

## Install
python -m pip install -r requirements.txt

## Run
python main.py

## Test GET endpoints
GET http://127.0.0.1:5000/
GET http://127.0.0.1:5000/random
GET http://127.0.0.1:5000/all
GET http://127.0.0.1:5000/search?name=multan

## POST /add
Send JSON:
{
  "name": "My Cafe",
  "location": "Multan",
  "coffee_price": "Rs. 400",
  "has_wifi": "True"
}

## PATCH /update-price/<cafe_id>
Send JSON:
{
  "coffee_price": "Rs. 550"
}

## DELETE /report-closed/<cafe_id>?api-key=my-secret-api-key

For learning only. Change the example API key before any public deployment.
