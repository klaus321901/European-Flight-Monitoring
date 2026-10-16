"""Run with: python -m unittest test_flight_monitoring.py"""
import tempfile
import unittest
from pathlib import Path
from database import initialize_database, upsert_flight, connect
from fetch_flights import normalize_flight


class FlightDatabaseTests(unittest.TestCase):
    def test_insert_and_update(self):
        with tempfile.TemporaryDirectory() as folder:
            db_path = Path(folder) / 'test.db'
            initialize_database(db_path)
            source = {
                'flight': {'iata': 'LH123'},
                'airline': {'name': 'Lufthansa'},
                'departure': {'iata': 'FRA', 'airport': 'Frankfurt', 'scheduled': '2026-10-16T10:00:00+02:00'},
                'arrival': {'iata': 'MUC', 'airport': 'Munich', 'scheduled': '2026-10-16T11:00:00+02:00'},
                'flight_status': 'scheduled'
            }
            record = normalize_flight(source)
            self.assertTrue(upsert_flight(record, db_path))
            record['actual_departure'] = '2026-10-16T10:20:00+02:00'
            self.assertTrue(upsert_flight(record, db_path))
            with connect(db_path) as db:
                self.assertEqual(db.execute('SELECT COUNT(*) FROM flights').fetchone()[0], 1)
                self.assertEqual(db.execute('SELECT COUNT(*) FROM airports').fetchone()[0], 2)
                self.assertEqual(db.execute('SELECT actual_departure FROM flights').fetchone()[0], record['actual_departure'])


if __name__ == '__main__':
    unittest.main()
