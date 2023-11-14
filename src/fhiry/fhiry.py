"""
 Copyright (c) 2020 Bell Eapen

 This software is released under the MIT License.
 https://opensource.org/licenses/MIT
"""

import pandas as pd
import json
import os
from .base_fhiry import BaseFhiry
import logging
from tqdm import tqdm

logger = logging.getLogger(__name__)

class Fhiry(BaseFhiry):
    def __init__(self, config_json=None):
        self._filename = ""
        self._folder = ""
        super().__init__(config_json=config_json)

    @property
    def df(self):
        return self._df

    @property
    def filename(self):
        return self._filename

    @property
    def folder(self):
        return self._folder

    @property
    def delete_col_raw_coding(self):
        return self._delete_col_raw_coding

    @filename.setter
    def filename(self, filename):
        self._filename = filename
        self._df = self.read_bundle_from_file(filename)

    @folder.setter
    def folder(self, folder):
        self._folder = folder

    @delete_col_raw_coding.setter
    def delete_col_raw_coding(self, delete_col_raw_coding):
        self._delete_col_raw_coding = delete_col_raw_coding

    def read_bundle_from_file(self, filename):
        with open(filename, encoding='utf8', mode='r') as f:
            json_in = f.read()
            json_in = json.loads(json_in)
            return pd.json_normalize(json_in['entry'])

    def process_source(self):
        """Read a single JSON resource or a directory full of JSON resources
        ONLY COMMON FIELDS IN ALL resources will be mapped
        """
        if self._folder:
            df = pd.DataFrame(columns=[])
            for file in tqdm(os.listdir(self._folder)):
                if file.endswith(".json"):
                    self._df = self.read_bundle_from_file(
                        os.path.join(self._folder, file))
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
        self._df = self.read_bundle_from_file(filename)
        self.process_df()
        return self._df

    def process_bundle_dict(self, bundle_dict):
        self._df = self.read_bundle_from_bundle_dict(bundle_dict)
        self.process_df()
        return self._df


