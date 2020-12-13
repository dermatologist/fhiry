
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

    def get_info(self):
        if self._df is None:
            return "Dataframe is empty"
        return self._df.info()

    def process_list(myList):
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
