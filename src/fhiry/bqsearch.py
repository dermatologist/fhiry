"""
 Copyright (c) 2023 Bell Eapen

 This software is released under the MIT License.
 https://opensource.org/licenses/MIT
"""


from google.cloud import bigquery

from .base_fhiry import BaseFhiry


class BQsearch(BaseFhiry):

    def __init__(self):
        # Construct a BigQuery client object.
        self._client = bigquery.Client()
        self._delete_col_raw_coding = True

    def search(self, query = None):
        if query is None:
            query = """
                SELECT *
                FROM `bigquery-public-data.fhir_synthea.patient`
                LIMIT 20
            """
        self._df = self._client.query(query).to_dataframe()
        super().process_df()
        return self._df

