
from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client()

query = """
    SELECT *
    FROM ``
    LIMIT 20
"""

df = client.query(query).to_dataframe()

print(df)