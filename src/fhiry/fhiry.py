"""
Copyright (c) 2020 Bell Eapen

This software is released under the MIT License.
https://opensource.org/licenses/MIT
"""

import json
import logging
import os

import pandas as pd
from tqdm import tqdm

from .base_fhiry import BaseFhiry

logger = logging.getLogger(__name__)


class Fhiry(BaseFhiry):
    """Read and process FHIR Bundles (.json) from file or folder.

    Args:
        config_json: Optional JSON string or file path with column transforms.
    """

    def __init__(self, config_json=None):
        self._filename = ""
        self._folder = ""
        super().__init__(config_json=config_json)

    @property
    def df(self):
        """pd.DataFrame | None: The current working dataframe, if any."""
        return self._df

    @property
    def filename(self):
        """str: The path to the currently selected input file, if any."""
        return self._filename

    @property
    def folder(self):
        """str: The path to the input folder containing Bundle JSON files."""
        return self._folder

    @property
    def delete_col_raw_coding(self):
        """bool: Whether to drop raw coding/display columns after extraction."""
        return self._delete_col_raw_coding

    @filename.setter
    def filename(self, filename):
        """Set the input file and load it into a dataframe.

        Args:
            filename (str): Path to a FHIR Bundle JSON file.
        """
        self._filename = filename
        self._df = self.read_bundle_from_file(filename)

    @folder.setter
    def folder(self, folder):
        """Set the input folder for processing Bundle JSON files.

        Args:
            folder (str): Path to a directory containing JSON files.
        """
        self._folder = folder

    @delete_col_raw_coding.setter
    def delete_col_raw_coding(self, delete_col_raw_coding):
        """Set whether to drop raw coding/display columns after extraction."""
        self._delete_col_raw_coding = delete_col_raw_coding

    def read_bundle_from_file(self, filename):
        """Load a FHIR Bundle JSON file and normalize its entries.

        Args:
            filename (str): Path to a FHIR Bundle JSON file.

        Returns:
            pd.DataFrame: Dataframe of the Bundle entries.
        """
        with open(filename, encoding="utf8", mode="r") as f:
            json_in = f.read()
            json_in = json.loads(json_in)
            return pd.json_normalize(json_in["entry"])

    def process_source(self):
        """Process either the selected file or the entire folder.

        Only columns common across resources will be mapped.
        """
        if self._folder:
            df = pd.DataFrame(columns=[])
            for file in tqdm(os.listdir(self._folder)):
                if file.endswith(".json"):
                    self._df = self.read_bundle_from_file(
                        os.path.join(self._folder, file)
                    )
                    self.process_df()
                    if df.empty:
                        df = self._df
                    else:
                        df = pd.concat([df, self._df])
            self._df = df
        elif self._filename:
            self._df = self.read_bundle_from_file(self._filename)
        super().process_df()

    def process_file(self, filename):
        """Process a single Bundle JSON file and return its dataframe."""
        self._df = self.read_bundle_from_file(filename)
        self.process_df()
        return self._df

    def process_bundle_dict(self, bundle_dict):
        """Process a FHIR Bundle dictionary and return its dataframe."""
        self._df = self.read_bundle_from_bundle_dict(bundle_dict)
        self.process_df()
        return self._df
