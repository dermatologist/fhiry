"""
 Copyright (c) 2023 Bell Eapen

 This software is released under the MIT License.
 https://opensource.org/licenses/MIT
"""


import multiprocessing as mp
import os

import pandas as pd

from . import Fhirndjson, Fhiry


def process_file(file, config_json=None):
    f = Fhiry(config_json=config_json)
    return f.process_file(file)


def process_ndjson(file, config_json=None):
    f = Fhirndjson(config_json=config_json)
    return f.process_file(file)


def process(folder):

    pool = mp.Pool(mp.cpu_count())

    filenames = []
    if os.path.isdir(folder):
        for filename in os.listdir(folder):
            if filename.endswith(".json"):
                filenames.append(folder + '/' + filename)
    else:
        filenames.append(folder)
        
    list_of_dataframes = pool.map(process_file, filenames)
    pool.close()
    return pd.concat(list_of_dataframes)


def ndjson(folder):
    pool = mp.Pool(mp.cpu_count())

    filenames = []

    if os.path.isdir(folder):
        for filename in os.listdir(folder):
            if filename.endswith(".ndjson"):
                filenames.append(folder + '/' + filename)
    else:
        filenames.append(folder)

    list_of_dataframes = pool.map(process_ndjson, filenames)
    pool.close()
    return pd.concat(list_of_dataframes)
