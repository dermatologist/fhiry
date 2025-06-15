"""
Copyright (c) 2020 Bell Eapen

This software is released under the MIT License.
https://opensource.org/licenses/MIT
"""

from typing import Any
import pandas as pd
import json
import logging

logger = logging.getLogger(__name__)


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
                with open(config_json, "r") as f:  # config_json is a file path
                    self.config = json.load(f)
            except:
                self.config = json.loads(config_json)  # config_json is a json string
        else:
            self.config = json.loads(
                '{ "REMOVE": ["resource.text.div"], "RENAME": { "resource.id": "id" } }'
            )

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
        return pd.json_normalize(bundle_dict["entry"])

    def delete_unwanted_cols(self):
        if self._df is None:
            logger.warning("Dataframe is empty, nothing to delete")
            return
        """Delete unwanted columns from the dataframe"""
        if "REMOVE" not in self.config:
            logger.warning("No columns to remove defined in config")
            return
        if not isinstance(self.config["REMOVE"], list):
            logger.warning(
                "REMOVE in config is not a list, expected a list of column names to remove"
            )
            return
        if len(self.config["REMOVE"]) == 0:
            logger.warning("No columns to remove defined in config")
            return
        logger.info("Removing columns: {}".format(self.config["REMOVE"]))
        for col in self.config["REMOVE"]:
            cols_to_remove = [
                c for c in self._df.columns if c == col or c.startswith(f"{col}.")
            ]
            for c in cols_to_remove:
                del self._df[c]

    def rename_cols(self):
        if self._df is not None:
            self._df.rename(columns=self.config["RENAME"], inplace=True)
        else:
            logger.warning("Dataframe is empty, nothing to rename")

    def remove_string_from_columns(self, string_to_remove="resource."):
        """Removes a string from all column names in a Pandas DataFrame.

        Args:
            df (pd.DataFrame): The input DataFrame.
            string_to_remove (str): The string to remove from column names.

        Returns:
            pd.DataFrame: A new DataFrame with modified column names.
        """
        if self._df is not None:
            self._df.columns = self._df.columns.str.replace(
                string_to_remove, "", regex=False
            )
        else:
            logger.warning("Dataframe is empty, cannot remove string from columns")
        return self._df

    def process_df(self):
        self.convert_object_to_list()
        self.add_patient_id()
        self.remove_string_from_columns(string_to_remove="resource.")
        self.empty_list_to_nan()
        self.drop_empty_cols()
        self.delete_unwanted_cols()
        self.rename_cols()
        return self._df

    def empty_list_to_nan(self):
        """Convert empty lists in the dataframe to NaN."""
        if self._df is None:
            logger.warning("Dataframe is empty, nothing to convert")
            return
        for col in self._df.columns:
            if self._df[col].dtype == "object":
                self._df[col] = self._df[col].apply(
                    lambda x: float("nan") if isinstance(x, list) and len(x) == 0 else x
                )

    def drop_empty_cols(self):
        """Drop columns that are completely empty (all NaN values) from the dataframe."""
        if self._df is None:
            logger.warning("Dataframe is empty, nothing to drop")
            return
        self._df.dropna(axis=1, how="all", inplace=True)
        if self._df is not None and self._df.empty:
            logger.warning("Dataframe is empty after dropping empty columns")
        return self._df

    def process_bundle_dict(self, bundle_dict):
        self._df = self.read_bundle_from_bundle_dict(bundle_dict)
        if self._df is None or self._df.empty:
            logger.warning("Dataframe is empty, nothing to process")
            return None
        self._df = self.process_df()
        return self._df

    def convert_object_to_list(self):
        if self._df is None:
            logger.warning("Dataframe is empty, nothing to convert")
            return
        """Convert object to a list of codes"""
        for col in self._df.columns:
            if "coding" in col:
                codes = self._df.apply(lambda x: self.process_list(x[col]), axis=1)
                self._df = pd.concat(
                    [self._df, codes.to_frame(name=col + ".codes")], axis=1
                )
                if self._delete_col_raw_coding:
                    del self._df[col]
            if "display" in col:
                codes = self._df.apply(lambda x: self.process_list(x[col]), axis=1)
                self._df = pd.concat(
                    [self._df, codes.to_frame(name=col + ".display")], axis=1
                )
                del self._df[col]

    def add_patient_id(self):
        """Create a patientId column with the resource.id if a Patient resource or with the resource.subject.reference if other resource type"""
        if self._df is None:
            logger.warning("Dataframe is empty, cannot add patientId")
            return
        try:
            # PerformanceWarning: DataFrame is highly fragmented.  This is usually the result of calling `frame.insert` many times, which has poor performance.  Consider joining all columns at once using pd.concat(axis=1) instead. To get a de-fragmented frame, use `newframe = frame.copy()`
            newframe = self._df.copy()
            newframe["patientId"] = self._df.apply(
                lambda x: (
                    x["resource.id"]
                    if x["resource.resourceType"] == "Patient"
                    else self.check_subject_reference(x)
                ),
                axis=1,
            )
            self._df = newframe
        except:
            try:
                newframe = self._df.copy()
                newframe["patientId"] = self._df.apply(
                    lambda x: (
                        x["id"]
                        if x["resourceType"] == "Patient"
                        else self.check_subject_reference(x)
                    ),
                    axis=1,
                )
                self._df = newframe
            except:
                pass

    def check_subject_reference(self, row):
        try:
            return (
                row["resource.subject.reference"]
                .replace("Patient/", "")
                .replace("urn:uuid:", "")
            )
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
                if "code" in entry:
                    myCodes.append(entry["code"])
                elif "display" in entry:
                    myCodes.append(entry["display"])
        return myCodes

    def llm_query(self, query, llm, embed_model=None, verbose=True):
        """Execute a query using llama_index

        Args:
            query (str): The natural language query
            llm (Any): The Language Model
            embed_model (str, optional): The embedding model string from HuggingFace. Defaults to None.
            verbose (bool, optional): Verbose or not. Defaults to True.

        Raises:
            Exception: Llama_index not installed
            Exception: Dataframe is empty

        Returns:
            Any: Results of the query
        """
        try:
            from llama_index.experimental.query_engine import PandasQueryEngine
            from llama_index.core import Settings
            from langchain_huggingface import HuggingFaceEmbeddings
        except Exception:
            raise Exception("llama_index or HuggingFaceEmbeddings not installed")
        if self._df is None:
            raise Exception("Dataframe is empty")
        if embed_model is None:
            embed_model = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")
        else:
            embed_model = HuggingFaceEmbeddings(model_name=embed_model)
        Settings.llm = llm
        Settings.embed_model = embed_model
        query_engine = PandasQueryEngine(
            df=self._df,
            verbose=verbose,
        )
        return query_engine.query(query)
