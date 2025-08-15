"""
Copyright (c) 2020 Bell Eapen

This software is released under the MIT License.
https://opensource.org/licenses/MIT
"""

import json
import os

import pandas as pd
from tqdm import tqdm

from .base_fhiry import BaseFhiry


class Fhirndjson(BaseFhiry):
    """Read and process NDJSON FHIR resources from a folder.

    Args:
        config_json: Optional JSON string or file path with column transforms.
    """

    def __init__(self, config_json=None):
        self._folder = ""
        super().__init__(config_json=config_json)

    @property
    def df(self):
        """pd.DataFrame | None: The current working dataframe, if any."""
        return self._df

    @property
    def folder(self):
        """str: The folder containing NDJSON files to process."""
        return self._folder

    @folder.setter
    def folder(self, folder):
        """Set the NDJSON input folder.

        Args:
            folder (str): Path to a directory with .ndjson files.
        """
        self._folder = folder

    def read_resource_from_line(self, line):
        """Normalize a single NDJSON line (JSON object) to a dataframe row."""
        return pd.json_normalize(json.loads(line))

    def process_source(self):
        """Process all NDJSON files in the folder into a single dataframe.

        Only columns common across resources will be mapped.
        """
        if self._folder:
            for file in tqdm(os.listdir(self._folder)):
                self.process_file(file)

    def process_file(self, file):
        """Process a single NDJSON file and append its rows to the dataframe.

        Args:
            file (str): Filename within the configured folder to process.

        Returns:
            pd.DataFrame | None: The updated dataframe.
        """
        df = self._df
        if file.endswith(".ndjson"):
            with open(os.path.join(self._folder, file)) as fp:
                Lines = fp.readlines()
                for line in tqdm(Lines):
                    self._df = self.read_resource_from_line(line)
                    self.process_df()
                    df = pd.concat([df, self._df])
        self._df = df
        return self._df
