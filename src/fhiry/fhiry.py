"""
 Copyright (c) 2020 Bell Eapen

 This software is released under the MIT License.
 https://opensource.org/licenses/MIT
"""


import pandas as pd
import json
import os


class Fhiry(object):
    def __init__(self):
        self._df = None
        self._filename = ""
        self._folder = ""

    @property
    def df(self):
        return self._df

    @property
    def filename(self):
        return self._filename

    @property
    def folder(self):
        return self._folder

    @filename.setter
    def filename(self, filename):
        self._filename = filename
        self._df = self.read_bundle_from_file(filename)

    @folder.setter
    def folder(self, folder):
        self._folder = folder

    def read_bundle_from_file(self, filename):
        with open(filename, 'r') as f:
            json_in = f.read()
            json_in = json.loads(json_in)
            return pd.json_normalize(json_in['entry'])

    def delete_unwanted_cols(self):
        if 'resource.text.div' in self._df.columns:
            del self._df['resource.text.div']

    def process_df(self):
        """Read a single JSON resource or a directory full of JSON resources
        ONLY COMMON FIELDS IN ALL resources will be mapped
        """
        if self._folder:
            df = pd.DataFrame(columns=[])
            for file in os.listdir(self._folder):
                if file.endswith(".json"):
                    self._df = self.read_bundle_from_file(
                        os.path.join(self._folder, file))
                    self.delete_unwanted_cols()
                    self.convert_object_to_list()
                    self.add_patient_id()
                    if df.empty:
                        df = self._df
                    else:
                        df = pd.concat([df, self._df])
            self._df = df
        elif self._filename:
            self._df = self.read_bundle_from_file(self._filename)
            self.delete_unwanted_cols()
            self.convert_object_to_list()
            self.add_patient_id()

    def process_file(self, filename):
        self._df = self.read_bundle_from_file(filename)
        self.delete_unwanted_cols()
        self.convert_object_to_list()
        self.add_patient_id()
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
        self._df['patientId'] = self._df[(
            self._df['resource.resourceType'] == "Patient")].iloc[0]['resource.id']

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
