from fastapi import FastAPI
import requests
import uvicorn
from dotenv import load_dotenv
import os
from urllib.parse import urlencode
import json

# Load the .env file
load_dotenv()

# Access the environment variable
# API_KEY = os.getenv('APP_ID')
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/test")
async def read_item():
    baseURL ='https://openexchangerates.org/api/latest.json'
    base = 'USD'
    access_key = os.getenv('APP_ID')
    params = {
        "app_id": access_key,  # The API key
        "symbols": "EUR,GBP,CAD,PLN,JPY,CNY"  # The currency symbols to fetch
    }

    # Construct the full URL with the parameters
    url = f"{baseURL}?{urlencode(params)}"

    # Make the request
    response = requests.get(url)
    if response.status_code != 200:
        return {'error': 'Failed to fetch data'}
    return response.json()

@app.get("/item/{item}")
def retrieve_item(item: str):
    response = requests.get('https://fakestoreapi.com/products')
    products = response.json()
    filtered_products = [
        product for product in products if item.lower() in product['title'].lower()
    ]
    
    return filtered_products

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)