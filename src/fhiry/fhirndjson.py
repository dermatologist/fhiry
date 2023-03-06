"""
 Copyright (c) 2020 Bell Eapen

 This software is released under the MIT License.
 https://opensource.org/licenses/MIT
"""


import pandas as pd
import json
import os
from .base_fhiry import BaseFhiry

class Fhirndjson(BaseFhiry):
    def __init__(self):
        self._df = pd.DataFrame(columns=[])
        self._folder = ""
        self._delete_col_raw_coding = True

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
            for file in os.listdir(self._folder):
                self.process_file(file)

    def process_file(self, file):
        df = self._df
        if file.endswith(".ndjson"):
            with open(os.path.join(self._folder, file)) as fp:
                Lines = fp.readlines()
                for line in Lines:
                    self._df = self.read_resource_from_line(line)
                    self.delete_unwanted_cols()
                    self.convert_object_to_list()
                    self.add_patient_id()
                    df = pd.concat([df, self._df])
        self._df = df
        return self._df

    #@overrides
    def add_patient_id(self):
        """Create a patientId column with the id if a Patient resource or with the subject.reference if other resource type
        """
        self._df['patientId'] = self._df.apply(lambda x: x['id'] if x['resourceType']
                                               == 'Patient' else self.check_subject_reference(x), axis=1)

