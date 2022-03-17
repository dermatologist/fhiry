from . import Fhiry, Fhirndjson
import os
import multiprocessing as mp
import pandas as pd

def process_files(file):
    f = Fhiry()
    return f.process_file(file)


def process_ndjson(file):
    f = Fhirndjson()
    return f.process_file(file)

def process(folder):
    # TODO: Fix the below error when ? folder has few files
    # Currently falls back when it fails
    # json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
    try:
        pool = mp.Pool(mp.cpu_count())
        list_of_dataframes = pool.map(process_files, [folder + '/' + row for row in os.listdir(folder)])
        pool.close()
        return pd.concat(list_of_dataframes)
    except:
        f = Fhiry()
        f.folder = folder
        f.process_df()
        return f.df


def ndjson(folder):
    # TODO: Fix the below error when ? folder has few files
    # Currently falls back when it fails
    # json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
    try:
        pool = mp.Pool(mp.cpu_count())
        list_of_dataframes = pool.map(
            process_ndjson, [folder + '/' + row for row in os.listdir(folder)])
        pool.close()
        return pd.concat(list_of_dataframes)
    except:
        f = Fhirndjson()
        f.folder = folder
        f.process_df()
        return f.df
