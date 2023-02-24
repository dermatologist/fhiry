from . import Fhiry, Fhirndjson
import os
import multiprocessing as mp
import pandas as pd


def process_file(file, columns_by_fhirpaths={}):
    f = Fhiry()
    f.columns_by_fhirpaths = columns_by_fhirpaths
    return f.process_file(file)


def process_ndjson(file):
    f = Fhirndjson()
    return f.process_file(file)


def process(folder, columns_by_fhirpaths={}):

    pool = mp.Pool(mp.cpu_count())

    filenames = []
    for filename in os.listdir(folder):
        if filename.endswith(".json"):
            # tuple with both arguments of function process_file(file, columns_by_fhirpaths)
            process_file_args = (folder + '/' + filename, columns_by_fhirpaths)
            # append to list of this tuples for starmap
            filenames.append(process_file_args)

    list_of_dataframes = pool.starmap(process_file, filenames)
    pool.close()
    return pd.concat(list_of_dataframes)


def ndjson(folder):
    pool = mp.Pool(mp.cpu_count())

    filenames = []
    for filename in os.listdir(folder):
        if filename.endswith(".ndjson"):
            filenames.append(folder + '/' + filename)

    list_of_dataframes = pool.map(process_ndjson, filenames)
    pool.close()
    return pd.concat(list_of_dataframes)
