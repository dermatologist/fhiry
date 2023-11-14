"""
 Copyright (c) 2020 Bell Eapen

 This software is released under the MIT License.
 https://opensource.org/licenses/MIT
"""

import pandas as pd
import json

class BaseFhiry(object):
    def __init__(self, config_json=None):
        self._df = None

        # Codes from the FHIR datatype "coding"
        # (f.e. element resource.code.coding or element resource.clinicalStatus.coding)
        # are extracted to a col "codingcodes"
        # (f.e. col resource.code.codingcodes or col resource.clinicalStatus.codingcodes)
        # without other for analysis often not needed metadata like f.e. codesystem URI
        # or FHIR extensions for coding entries.
        # The full / raw object in col "coding" is deleted after this extraction.
        # If you want to analyze more than the content of code and display from codings
        # (like f.e. different codesystem URIs or further codes in extensions
        # in the raw data/object), you can disable deletion of the raw source object "coding"
        # (f.e. col "resource.code.coding") by setting property delete_col_raw_coding to False
        self._delete_col_raw_coding = True
        if config_json is not None:
            try:
                with open(config_json, 'r') as f: # config_json is a file path
                    self.config = json.load(f)
            except:
                self.config = json.loads(config_json)   # config_json is a json string
        else:
            self.config = json.loads('{ "REMOVE": ["resource.text.div"], "RENAME": { "resource.id": "id" } }')

    @property
    def df(self):
        return self._df

    @property
    def delete_col_raw_coding(self):
        return self._delete_col_raw_coding

    @delete_col_raw_coding.setter
    def delete_col_raw_coding(self, delete_col_raw_coding):
        self._delete_col_raw_coding = delete_col_raw_coding

    def read_bundle_from_bundle_dict(self, bundle_dict):
        return pd.json_normalize(bundle_dict['entry'])

    def delete_unwanted_cols(self):
        for col in self.config['REMOVE']:
            if col in self._df.columns:
                del self._df[col]

    def rename_cols(self):
        self._df.rename(columns=self.config['RENAME'], inplace=True)

    def process_df(self):
        self.delete_unwanted_cols()
        self.convert_object_to_list()
        self.add_patient_id()
        self.rename_cols()


    def process_bundle_dict(self, bundle_dict):
        self._df = self.read_bundle_from_bundle_dict(bundle_dict)
        self.delete_unwanted_cols()
        self.convert_object_to_list()
        self.add_patient_id()
        self.rename_cols()
        return self._df

    def convert_object_to_list(self):
        """Convert object to a list of codes
        """
        for col in self._df.columns:
            if 'coding' in col:
                codes = self._df.apply(
                    lambda x: self.process_list(x[col]), axis=1)
                self._df = pd.concat(
                    [self._df, codes.to_frame(name=col+'codes')], axis=1)
                if self._delete_col_raw_coding:
                    del self._df[col]
            if 'display' in col:
                codes = self._df.apply(
                    lambda x: self.process_list(x[col]), axis=1)
                self._df = pd.concat(
                    [self._df, codes.to_frame(name=col+'display')], axis=1)
                del self._df[col]

    def add_patient_id(self):
        """Create a patientId column with the resource.id if a Patient resource or with the resource.subject.reference if other resource type
        """
        try:
            # PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
            newframe = self._df.copy()
            newframe['patientId'] = self._df.apply(lambda x: x['resource.id'] if x['resource.resourceType']
                                               == 'Patient' else self.check_subject_reference(x), axis=1)
            self._df = newframe
        except:
            try:
                newframe = self._df.copy()
                newframe['patientId'] = self._df.apply(lambda x: x['id'] if x['resourceType']
                                                    == 'Patient' else self.check_subject_reference(x), axis=1)
                self._df = newframe
            except:
                pass

    def check_subject_reference(self, row):
        try:
            return row['resource.subject.reference'].replace('Patient/', '')
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
                elif 'display' in entry:
                    myCodes.append(entry['display'])
        return myCodes
