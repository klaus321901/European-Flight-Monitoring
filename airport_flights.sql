CREATE TABLE IF NOT EXISTS airports (
    iata_code TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    city TEXT NOT NULL,
    country TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS flights (
    flight_id SERIAL PRIMARY KEY,
    flight_number TEXT NOT NULL,
    airline TEXT NOT NULL,
    departure_airport TEXT REFERENCES airports(iata_code),
    arrival_airport TEXT REFERENCES airports(iata_code),
    departure_time TIMESTAMP NOT NULL,
    arrival_time TIMESTAMP NOT NULL,
    status TEXT NOT NULL,
    UNIQUE(flight_number, departure_time)
);
INSERT INTO airports (iata_code, name, city, country) VALUES
('FRA', 'Frankfurt Airport', 'Frankfurt', 'Germany'),
('MUC', 'Munich Airport', 'Munich', 'Germany'),
('TXL', 'Berlin Tegel Airport', 'Berlin', 'Germany'),
('HAM', 'Hamburg Airport', 'Hamburg', 'Germany'),
('DUS', 'Düsseldorf Airport', 'Düsseldorf', 'Germany');

INSERT INTO flights (flight_number, airline, departure_airport, arrival_airport, departure_time, arrival_time, status) VALUES
('LH123', 'Lufthansa', 'FRA', 'MUC', '2025-03-22 08:00:00', '2025-03-22 09:15:00', 'on-time'),
('LH456', 'Lufthansa', 'MUC', 'TXL', '2025-03-22 10:00:00', '2025-03-22 11:30:00', 'delayed'),
('AF789', 'Air France', 'TXL', 'DUS', '2025-03-22 12:00:00', '2025-03-22 13:45:00', 'on-time'),
('BA234', 'British Airways', 'HAM', 'FRA', '2025-03-22 14:30:00', '2025-03-22 16:00:00', 'delayed'),
('EK567', 'Emirates', 'DUS', 'MUC', '2025-03-22 17:00:00', '2025-03-22 18:50:00', 'on-time'),
('QR890', 'Qatar Airways', 'MUC', 'HAM', '2025-03-22 20:00:00', '2025-03-22 21:45:00', 'delayed'),
('DL345', 'Delta Airlines', 'TXL', 'FRA', '2025-03-22 22:00:00', '2025-03-23 00:00:00', 'on-time'),
('UA678', 'United Airlines', 'FRA', 'TXL', '2025-03-23 05:30:00', '2025-03-23 07:15:00', 'delayed'),
('KLM901', 'KLM', 'HAM', 'DUS', '2025-03-23 08:00:00', '2025-03-23 09:30:00', 'on-time'),
('TK123', 'Turkish Airlines', 'DUS', 'MUC', '2025-03-23 10:00:00', '2025-03-23 11:45:00', 'delayed');


SELECT * FROM flights WHERE departure_airport = 'FRA';

SELECT * FROM flights 
WHERE status = 'delayed' 
AND (arrival_time - departure_time) > INTERVAL '2 hours';

SELECT * FROM flights WHERE flight_number = 'LH123';



