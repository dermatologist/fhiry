
from .base_fhiry import BaseFhiry
from google.cloud import bigquery



query = """
    SELECT *
    FROM ``
    LIMIT 20
"""

class BQsearch(BaseFhiry):

    def __init__(self):
        # Construct a BigQuery client object.
        self._client = bigquery.Client()
        self._delete_col_raw_coding = True

    def search(self, query):
        self._df = self._client.query(query).to_dataframe()
        super().process_df()
        return self._df

