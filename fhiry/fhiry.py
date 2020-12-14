
import pandas as pd
import json


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
        del self._df['resource.text.div']

    def process_df(self):
        if self._filename:
            self._df = self.read_bundle_from_file(self._filename)
            self.delete_unwanted_cols()
            self.convert_object_to_list()
            self.add_patient_id()

    def convert_object_to_list(self):
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
