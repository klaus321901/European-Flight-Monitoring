"""Fetch flight records from AviationStack and persist them in SQLite."""
import os
import requests
from database import initialize_database, upsert_flight

API_URL = 'https://api.aviationstack.com/v1/flights'


def normalize_flight(item):
    """Map nested AviationStack JSON into the database column names."""
    departure = item.get('departure') or {}
    arrival = item.get('arrival') or {}
    flight = item.get('flight') or {}
    airline = item.get('airline') or {}
    return {
        'flight_number': flight.get('iata'),
        'airline': airline.get('name'),
        'departure_airport': departure.get('iata'),
        'departure_name': departure.get('airport'),
        'arrival_airport': arrival.get('iata'),
        'arrival_name': arrival.get('airport'),
        'scheduled_departure': departure.get('scheduled'),
        'actual_departure': departure.get('actual'),
        'scheduled_arrival': arrival.get('scheduled'),
        'actual_arrival': arrival.get('actual'),
        'status': item.get('flight_status'),
    }


def fetch_flight_data(api_key=None, max_pages=1):
    api_key = api_key or os.getenv('AVIATIONSTACK_API_KEY')
    if not api_key:
        raise ValueError('Set AVIATIONSTACK_API_KEY before running this script.')
    initialize_database()
    saved = 0
    for page in range(max_pages):
        response = requests.get(API_URL, params={'access_key': api_key, 'limit': 100, 'offset': page * 100}, timeout=30)
        response.raise_for_status()
        payload = response.json()
        if payload.get('error'):
            raise RuntimeError(f"AviationStack error: {payload['error']}")
        items = payload.get('data') or []
        for item in items:
            if upsert_flight(normalize_flight(item)):
                saved += 1
        if len(items) < 100:
            break
    print(f'Processed {saved} flight records into SQLite.')
    return saved


if __name__ == '__main__':
    fetch_flight_data()
