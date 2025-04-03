import os
import requests
import json

# Fetch the API key from environment variables
API_KEY = os.getenv("AVIATIONSTACK_API_KEY")

# AviationStack API URL
API_URL = f"http://api.aviationstack.com/v1/flights?access_key={API_KEY}"

def fetch_flight_data():
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            flights = response.json()
            
            # Extract and print essential flight details
            for flight in flights.get("data", []):  # "data" contains flight details
                print(f"\nFlight: {flight.get('flight', {}).get('iata', 'N/A')}")
                print(f"From: {flight.get('departure', {}).get('airport', 'N/A')} ({flight.get('departure', {}).get('iata', 'N/A')})")
                print(f"To: {flight.get('arrival', {}).get('airport', 'N/A')} ({flight.get('arrival', {}).get('iata', 'N/A')})")
                print(f"Departure Time: {flight.get('departure', {}).get('scheduled', 'N/A')}")
                print(f"Arrival Time: {flight.get('arrival', {}).get('scheduled', 'N/A')}")
                print("-" * 50)

        else:
            print("Failed to fetch data. Status Code:", response.status_code)

    except Exception as e:
        print("Error:", e)

# Run the function
fetch_flight_data()
