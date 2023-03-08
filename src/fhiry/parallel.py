"""
 Copyright (c) 2023 Bell Eapen

 This software is released under the MIT License.
 https://opensource.org/licenses/MIT
"""

import multiprocessing as mp
import os
import pandas as pd
from . import Fhirndjson, Fhiry

def process(folder, config_json=None):

    pool = mp.Pool(mp.cpu_count())
    f = Fhiry(config_json=config_json)
    filenames = []
    if os.path.isdir(folder):
        for filename in os.listdir(folder):
            if filename.endswith(".json"):
                filenames.append(folder + '/' + filename)
    else:
        filenames.append(folder)

    list_of_dataframes = pool.map(f.process_file, filenames)
    pool.close()
    return pd.concat(list_of_dataframes)


def ndjson(folder, config_json=None):
    pool = mp.Pool(mp.cpu_count())
    f = Fhirndjson(config_json=config_json)
    filenames = []

    if os.path.isdir(folder):
        for filename in os.listdir(folder):
            if filename.endswith(".ndjson"):
                filenames.append(folder + '/' + filename)
    else:
        filenames.append(folder)

    list_of_dataframes = pool.map(f.process_file, filenames)
    pool.close()
    return pd.concat(list_of_dataframes)
