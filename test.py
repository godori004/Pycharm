from google.cloud import bigquery

client = bigquery.Client()

# Perform a query.
QUERY = (
    'SELECT * FROM `hanwha-life.195231946.ga_sessions_20200405` '    
    'LIMIT 10')
print(QUERY)
query_job = client.query(QUERY)  # API request


rows = query_job.result()  # Waits for query to finish

for row in rows:

    print(row);

