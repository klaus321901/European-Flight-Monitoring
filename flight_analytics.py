"""Analyze observed flight departure and arrival delays from SQLite records."""
from database import connect, initialize_database


def delay_summary():
    initialize_database()
    # julianday handles ISO 8601 timestamps with timezone offsets supported by SQLite.
    with connect() as db:
        db.row_factory = __import__('sqlite3').Row
        query = '''
        SELECT airline, COUNT(*) AS flights_with_actual_departure,
               ROUND(AVG(MAX(0, (julianday(actual_departure) - julianday(scheduled_departure))*1440)), 1)
                   AS average_departure_delay_minutes,
               SUM(CASE WHEN (julianday(actual_departure) - julianday(scheduled_departure))*1440 > 15
                   THEN 1 ELSE 0 END) AS departures_over_15_minutes
        FROM flights
        WHERE actual_departure IS NOT NULL AND julianday(actual_departure) IS NOT NULL
          AND julianday(scheduled_departure) IS NOT NULL
        GROUP BY airline ORDER BY average_departure_delay_minutes DESC
        '''
        return [dict(row) for row in db.execute(query)]


if __name__ == '__main__':
    for result in delay_summary():
        print(result)
