import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).with_name('flights.db')


def connect(path=DB_PATH):
    connection = sqlite3.connect(path)
    connection.execute('PRAGMA foreign_keys = ON')
    return connection


def initialize_database(path=DB_PATH):
    with connect(path) as db:
        db.executescript('''
        CREATE TABLE IF NOT EXISTS airports (
            iata_code TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            city TEXT,
            country TEXT
        );
        CREATE TABLE IF NOT EXISTS flights (
            flight_id INTEGER PRIMARY KEY AUTOINCREMENT,
            flight_number TEXT NOT NULL,
            airline TEXT,
            departure_airport TEXT REFERENCES airports(iata_code),
            arrival_airport TEXT REFERENCES airports(iata_code),
            scheduled_departure TEXT NOT NULL,
            actual_departure TEXT,
            scheduled_arrival TEXT,
            actual_arrival TEXT,
            status TEXT,
            UNIQUE(flight_number, scheduled_departure)
        );
        CREATE INDEX IF NOT EXISTS idx_flights_origin_time
            ON flights(departure_airport, scheduled_departure);
        CREATE INDEX IF NOT EXISTS idx_flights_airline_time
            ON flights(airline, scheduled_departure);
        CREATE INDEX IF NOT EXISTS idx_flights_status ON flights(status);
        ''')


def upsert_flight(record, path=DB_PATH):
    """Persist one validated API record; airport references are created first."""
    flight_number = record.get('flight_number')
    scheduled_departure = record.get('scheduled_departure')
    if not flight_number or not scheduled_departure:
        return False
    with connect(path) as db:
        for prefix in ('departure', 'arrival'):
            code = record.get(f'{prefix}_airport')
            if code:
                db.execute('''INSERT INTO airports(iata_code,name,city,country)
                    VALUES(?,?,?,?) ON CONFLICT(iata_code) DO UPDATE SET
                    name=CASE WHEN excluded.name != '' THEN excluded.name ELSE airports.name END,
                    city=COALESCE(excluded.city,airports.city),
                    country=COALESCE(excluded.country,airports.country)''',
                    (code, record.get(f'{prefix}_name') or code,
                     record.get(f'{prefix}_city'), record.get(f'{prefix}_country')))
        columns = ('flight_number','airline','departure_airport','arrival_airport',
                   'scheduled_departure','actual_departure','scheduled_arrival',
                   'actual_arrival','status')
        db.execute('''INSERT INTO flights ('''+','.join(columns)+''') VALUES ('''+','.join('?' for _ in columns)+''')
            ON CONFLICT(flight_number,scheduled_departure) DO UPDATE SET
                airline=excluded.airline,
                departure_airport=excluded.departure_airport,
                arrival_airport=excluded.arrival_airport,
                actual_departure=COALESCE(excluded.actual_departure,flights.actual_departure),
                scheduled_arrival=COALESCE(excluded.scheduled_arrival,flights.scheduled_arrival),
                actual_arrival=COALESCE(excluded.actual_arrival,flights.actual_arrival),
                status=excluded.status''', tuple(record.get(k) for k in columns))
    return True
