"""
Copyright (c) 2023 Bell Eapen

This software is released under the MIT License.
https://opensource.org/licenses/MIT
"""

from google.cloud import bigquery

from .base_fhiry import BaseFhiry


class BQsearch(BaseFhiry):
    """Query FHIR datasets in Google BigQuery and process results."""

    def __init__(self, config_json=None):
        # Construct a BigQuery client object.
        self._client = bigquery.Client()
        super().__init__(config_json=config_json)

    def search(self, query=None):
        """Run a BigQuery SQL query and return a processed dataframe.

        Args:
            query (str | None): Either a SQL string, a path to a .sql file, or
                None to run a default sample query.

        Returns:
            pd.DataFrame: The query results after standard processing.
        """
        if query is None:
            _query = """
                SELECT *
                FROM `bigquery-public-data.fhir_synthea.patient`
                LIMIT 20
            """
        else:
            try:
                with open(query, "r") as f:
                    _query = f.read()
            except:
                _query = query

        self._df = self._client.query(_query).to_dataframe()
        super().process_df()
        return self._df
