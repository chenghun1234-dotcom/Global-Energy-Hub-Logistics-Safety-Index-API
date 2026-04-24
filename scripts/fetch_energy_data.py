import requests
import json
import os
from datetime import datetime

# Environment variables for API keys
EIA_API_KEY = os.getenv('EIA_API_KEY')
OPINET_API_KEY = os.getenv('OPINET_API_KEY')

DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'prices.json')

def fetch_eia_data():
    """
    Fetch Brent Crude prices from EIA API.
    Ref: https://www.eia.gov/opendata/
    """
    if not EIA_API_KEY:
        print("EIA_API_KEY not found. Skipping.")
        return None
    
    # Petroleum Spot Price: RBRTE (Brent)
    url = f"https://api.eia.gov/v2/petroleum/pri/spt/data/?api_key={EIA_API_KEY}&frequency=daily&data[]=value&facets[series][]=RBRTE&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=1"
    
    try:
        response = requests.get(url)
        data = response.json()
        if 'response' in data and 'data' in data['response'] and len(data['response']['data']) > 0:
            current_price = data['response']['data'][0]['value']
            return float(current_price)
        return None
    except Exception as e:
        print(f"Error fetching EIA data: {e}")
        return None

def fetch_opinet_data():
    """
    Fetch Korea average oil prices from Opinet.
    Ref: http://www.opinet.co.kr/api/avgAllPrice.do
    """
    if not OPINET_API_KEY:
        print("OPINET_API_KEY not found. Skipping.")
        return None
    
    url = f"http://www.opinet.co.kr/api/avgAllPrice.do?out=json&code={OPINET_API_KEY}"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        gasoline = 0
        diesel = 0
        
        if 'RESULT' in data and 'OIL' in data['RESULT']:
            for item in data['RESULT']['OIL']:
                # B027 is Gasoline, D047 is Diesel
                if item['PRODCD'] == 'B027':
                    gasoline = float(item['PRICE'])
                elif item['PRODCD'] == 'D047':
                    diesel = float(item['PRICE'])
            
            return {"gasoline": gasoline, "diesel": diesel}
        return None
    except Exception as e:
        print(f"Error fetching Opinet data: {e}")
        return None

def update_json():
    with open(DATA_FILE, 'r') as f:
        prices = json.load(f)
    
    eia_brent = fetch_eia_data()
    if eia_brent:
        prices['crude_oil']['brent'] = eia_brent
        
    opinet_data = fetch_opinet_data()
    if opinet_data:
        prices['korea_average']['gasoline'] = opinet_data['gasoline']
        prices['korea_average']['diesel'] = opinet_data['diesel']
    
    prices['updated_at'] = datetime.utcnow().isoformat() + "Z"
    
    with open(DATA_FILE, 'w') as f:
        json.dump(prices, f, indent=2)
    
    print(f"Data updated at {prices['updated_at']}")

if __name__ == "__main__":
    update_json()
    print("Sync complete.")
