"""
 Copyright (c) 2020 Bell Eapen

 This software is released under the MIT License.
 https://opensource.org/licenses/MIT
"""


import pandas as pd
import json
import os


class Fhirndjson(object):
    def __init__(self):
        self._df = pd.DataFrame(columns=[])
        self._folder = ""

    @property
    def df(self):
        return self._df

    @property
    def folder(self):
        return self._folder

    @folder.setter
    def folder(self, folder):
        self._folder = folder

    def delete_unwanted_cols(self):
        if 'text.div' in self._df.columns:
            del self._df['text.div']

    def read_resource_from_line(self, line):
        return pd.json_normalize(json.loads(line))

    def process_df(self):
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

    def convert_object_to_list(self):
        """Convert object to a list of codes
        """
        for col in self._df.columns:
            if 'coding' in col:
                codes = self._df.apply(
                    lambda x: self.process_list(x[col]), axis=1)
                self._df = pd.concat(
                    [self._df, codes.to_frame(name=col+'codes')], 1)
                del self._df[col]
            if 'display' in col:
                codes = self._df.apply(
                    lambda x: self.process_list(x[col]), axis=1)
                self._df = pd.concat(
                    [self._df, codes.to_frame(name=col+'display')], 1)
                del self._df[col]

    def add_patient_id(self):
        """Create a patientId column with the resource.id of the first Patient resource
        """
        self._df['patientId'] = self._df.apply(lambda x: x['id'] if x['resourceType']
                                               == 'Patient' else self.check_subject_reference(x), axis=1)

    def check_subject_reference(self, row):
        try:
            return row['subject.reference'].replace('Patient/', '')
        except:
            return ""

    def get_info(self):
        if self._df is None:
            return "Dataframe is empty"
        return self._df.info()

    def process_list(self, myList):
        """Extracts the codes from a list of objects

        Args:
            myList (list): A list of objects

        Returns:
            list: A list of codes
        """
        myCodes = []
        if isinstance(myList, list):
            for entry in myList:
                if 'code' in entry:
                    myCodes.append(entry['code'])
                else:
                    myCodes.append(entry['display'])
        return myCodes
