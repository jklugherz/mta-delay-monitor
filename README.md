# mta-delay-monitor

This repository holds two applications: a monitor which continuously monitors the status of MTA service to see whether a line is delayed or not and prints updates to the console, and an API with two endpoints:
- /status - takes the name of a particular line as an argument and returns whether or not the line is currently delayed
- /uptime - takes the name of a particular line as an argument and returns the fraction of time that it has not been delayed since inception.

I plan to use Google Cloud resources to store data (Cloud SQL) and deploy (App Engine) the cron job (aka. the monitor) and the Flask API. 

### Next Steps
- DB connection: Create two tables in Cloud SQL and connect in code using pyodbc.
  - tbl_mta_subway_line
    - line_id (string, identity)
    - created_at (datetime)
    - is_delayed (boolean)

  - tbl_mta_subway_delay_alert
    - line_id (primary key)
    - alert id (primary key)
    - start (datetime)
    - end (datetime)
    - duration (int in seconds)
    
- Deployment: Deploy as two separate apps -
   - The monitor should run on a schedule, perhaps every 10 seconds. Use Google App Engine Cron Service to deploy.
   - The API can be deployed on Google App Engine.
- Refactoring: 
  - I open multiple DB connections when updating delay duration for multiple lines, when I should just open one. 
  - Add error handling for db connections, serializing JSON to Python object.
  - Add unit/integration tests.
  
  
### Scaling/Performance Improvements
If I have many users requesting status at one time, I'll be performing a lot of database reads. To mitigate this, I could cache the record (from  whenever it's updated (subway line, is_delayed, via tbl_mta_subway_line). 

I could also pre-calculate uptime (either whenever I update duration of a delay, or in a separate job) and store it on the main subway line table (tbl_mta_subway_line), and cache this value as well.

### Questions
- What is an acceptable latency for retrieving status or uptime?
