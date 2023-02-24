"""
 Copyright (c) 2020 Bell Eapen

 This software is released under the MIT License.
 https://opensource.org/licenses/MIT
"""


import pandas as pd
import json
import os
import fhirpathpy

class Fhiry(object):
    def __init__(self):
        self._df = None
        self._filename = ""
        self._folder = ""

        self._columns_by_fhirpaths = {}

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
    def columns_by_fhirpaths(self):
        return self._columns_by_fhirpaths

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

    @columns_by_fhirpaths.setter
    def columns_by_fhirpaths(self, columns_by_fhirpaths):
        self._columns_by_fhirpaths = columns_by_fhirpaths

    def read_bundle_from_file(self, filename):
        with open(filename, 'r') as f:
            bundle_dict = json.load(f)

        df = self.read_bundle_from_bundle_dict(bundle_dict)

        return df

    def read_bundle_from_bundle_dict(self, bundle_dict):

        # Flatten nested object structure to flat table structure
        df = pd.json_normalize(bundle_dict['entry'])

        # if (optional/additional) Fhirpath to dataframe column mappings,
        # add values from FHIR paths to mapped columns
        for col, fhirpath in self._columns_by_fhirpaths.items():
            df[col] = None
            i = 0
            for entry in bundle_dict['entry']:
                df.at[i, col] = fhirpathpy.evaluate(entry['resource'], path=fhirpath)
                i += 1

        return df

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

    def process_bundle_dict(self, bundle_dict):
        self._df = self.read_bundle_from_bundle_dict(bundle_dict)
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
        self._df['patientId'] = self._df.apply(lambda x: x['resource.id'] if x['resource.resourceType']
                                               == 'Patient' else self.check_subject_reference(x), axis=1)

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
