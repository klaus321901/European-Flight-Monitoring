# European Flight Monitoring System

## Database Design

### Schema Overview
The database schema is designed to store and manage data for European airports, flight schedules, flight statuses, and delays. It ensures efficient data retrieval and scalability for real-time flight tracking and monitoring.

### Tables and Their Relationships

#### Airports Table
| Column       | Type   | Description |
|-------------|--------|-------------|
| iata_code   | STRING | Primary key. Unique identifier for each airport. |
| name        | STRING | Name of the airport. |
| city        | STRING | City where the airport is located. |
| country     | STRING | Country where the airport is located. |

#### Flights Table
| Column             | Type   | Description |
|--------------------|--------|-------------|
| flight_number      | STRING | Unique identifier for the flight. |
| airline           | STRING | Name of the airline operating the flight. |
| departure_airport | STRING | Foreign key referencing `airports(iata_code)`. |
| arrival_airport   | STRING | Foreign key referencing `airports(iata_code)`. |
| departure_time    | TIMESTAMP | Scheduled departure time. |
| arrival_time      | TIMESTAMP | Scheduled arrival time. |
| status           | STRING | Current status of the flight (e.g., "on time", "delayed"). |

### Ensuring Data Accuracy and Scalability
- **Data Integrity:**
  - Using primary and foreign keys ensures valid relationships between airports and flights.
  - The `NOT NULL` constraint prevents missing essential data.
- **Normalization:**
  - Data is normalized to avoid redundancy. Instead of storing airport details in the flights table, they are referenced using IATA codes.
- **Indexing and Performance Optimization:**
  - Indexing `flight_number` and `departure_time` speeds up flight searches.
  - Query performance is improved using optimized joins between the `flights` and `airports` tables.
- **Scalability Considerations:**
  - The schema is flexible to accommodate new fields like flight delays, weather conditions, or additional airline details.
  - A partitioned table can be used for large datasets, splitting flights by year or month for better query performance.

## Data Collection Strategy

### Collecting European Airport Data
The `airports` table is initially populated with static data. For full coverage of European airports, data can be sourced from:
- **Open Data Repositories:**
  - ICAO, IATA databases
  - OpenSky Network, Eurocontrol data feeds
- **Automated API Data Collection:**
  - Periodic API calls to third-party services like FlightAware, OpenSky, or AviationStack can keep airport details updated.

### Real-Time Flight Data Collection
- **Using External APIs:**
  - APIs like FlightAware, OpenSky Network, and AviationStack provide real-time flight schedules, statuses, and delay reports.
- **Scraping Public Data (If APIs Are Not Available):**
  - A custom web scraper can extract flight schedules from airline and airport websites.
  - AI-based scraping tools (like ChatGPT API for text processing) can refine unstructured data.

### Handling Missing, Delayed, or Inconsistent Data
- **Missing Data:**
  - If an API does not return certain flight details, the system can:
    - Assign a default value (e.g., "Unknown" for missing airline names).
    - Mark the flight as pending and re-fetch data later.
- **Delayed Data:**
  - If an API update is delayed, timestamps from multiple sources (e.g., airline websites + government databases) can be cross-checked.
- **Inconsistent Data:**
  - Data validation ensures that departure time is always before arrival time.
  - A log system can track incorrect updates, flagging them for manual review.

## Flight Monitoring and Claim Identification

### Monitoring Flight Delays
The system continuously tracks flights and flags those with delays exceeding 2 hours.

### Technical Approach for Real-Time Monitoring

#### Data Collection
- APIs like AviationStack provide real-time updates on flight statuses.
- The database records flight departure, arrival times, and delay status.

#### Real-Time Processing
```sql
SELECT * FROM flights 
WHERE status = 'delayed' 
AND (arrival_time - departure_time) > INTERVAL '2 hours';
```
- Flights flagged as delayed trigger a notification system.

#### Automated Alerts
- The system can send notifications via email, SMS, or Telegram bot.
- **Example notification rule:**
  - If a flight is delayed by 2+ hours, send an alert to passengers.
  - If a flight is canceled, notify users immediately.

### Efficiently Storing and Managing Large Volumes of Data
- **Partitioning:**
  - Split the `flights` table by date (e.g., `flights_2025`, `flights_2026`).
  - Improves query speed for past flight records.
- **Indexing & Caching:**
  - Use indexes on `flight_number`, `departure_time`, and `status` to speed up searches.
  - Redis/Memcached caching can reduce API response time for frequently queried flight data.
- **Log-Based Storage:**
  - Store historical flight delays in a separate log table for trend analysis.
  - Helps airlines predict delay patterns based on historical data.

## Future API Development

### Designing a Scalable API for Flight Data
A REST API can expose flight data to users, airlines, and third-party applications.

### Key API Endpoints
| Endpoint                 | Description |
|--------------------------|-------------|
| `/api/flights`           | Get all flights. |
| `/api/flights/{flight_number}` | Get details of a specific flight. |
| `/api/flights/delayed`   | Fetch all flights delayed by more than 2 hours. |
| `/api/airports`          | Retrieve the list of all European airports. |

### API Implementation Strategy
- **Backend Framework:** Use FastAPI (Python) or Django REST Framework.
- **Database Integration:** Query PostgreSQL efficiently using async queries.
- **Pagination:** Implement pagination to handle large flight datasets.

### Ensuring API Security, Availability, and Reliability
#### Security Measures
- **Authentication:** Use API keys or OAuth2 for user authentication.
- **Rate Limiting:** Prevent abuse by limiting the number of API calls per minute.

#### Availability & Load Balancing
- **Horizontal Scaling:** Deploy multiple API servers to distribute traffic.
- **Load Balancer:** Use Nginx or AWS ELB to distribute requests efficiently.

#### Reliability Enhancements
- **Database Replication:** Maintain read replicas for high availability.
- **Failover Mechanism:** If the primary database goes down, the system automatically switches to a backup.

## Evaluation Criteria & How the Project Meets Them

| Criteria              | Implementation Details |
|----------------------|----------------------|
| Database Design      | The schema is normalized, ensuring efficient data retrieval with primary/foreign keys. |
| Data Collection Strategy | Uses third-party APIs, data validation techniques, and automated missing data handling. |
| Coding Skills        | SQL queries are optimized, and API integration follows best practices. |
| Problem-Solving      | Implements real-time monitoring, alert systems, and scalable data storage solutions. |

## Conclusion
The European Flight Monitoring System is a scalable, reliable, and efficient solution for tracking flight delays, managing airport data, and providing an API for external applications.

### Next Steps:
- Implement historical delay prediction using AI models.
- Expand API functionality to include weather-based flight delay predictions.
- Optimize database performance using distributed storage solutions.
