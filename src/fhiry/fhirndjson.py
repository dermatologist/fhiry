"""
 Copyright (c) 2020 Bell Eapen

 This software is released under the MIT License.
 https://opensource.org/licenses/MIT
"""


import pandas as pd
import json
import os
from .base_fhiry import BaseFhiry
from tqdm import tqdm

class Fhirndjson(BaseFhiry):
    def __init__(self, config_json=None):
        self._folder = ""
        super().__init__(config_json=config_json)

    @property
    def df(self):
        return self._df

    @property
    def folder(self):
        return self._folder

    @folder.setter
    def folder(self, folder):
        self._folder = folder


    def read_resource_from_line(self, line):
        return pd.json_normalize(json.loads(line))

    def process_source(self):
        """Read a single JSON resource or a directory full of JSON resources
        ONLY COMMON FIELDS IN ALL resources will be mapped
        """
        if self._folder:
            for file in tqdm(os.listdir(self._folder)):
                self.process_file(file)

    def process_file(self, file):
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


