import multiprocessing as mp
import os
import pandas as pd
from . import Fhirndjson, Fhiry
import logging
from tqdm import tqdm  # Add this import

logger = logging.getLogger(__name__)


def process(folder, config_json=None):
    logger.info("CPU count: {}".format(mp.cpu_count()))
    f = Fhiry(config_json=config_json)
    filenames = []
    if os.path.isdir(folder):
        for filename in os.listdir(folder):
            if filename.endswith(".json"):
                filenames.append(folder + "/" + filename)
    else:
        filenames.append(folder)

    with mp.Pool(mp.cpu_count()) as pool:
        list_of_dataframes = list(
            tqdm(
                pool.imap(f.process_file, filenames),
                total=len(filenames),
                desc="Processing JSON files",
            )
        )
    return pd.concat(list_of_dataframes)


def ndjson(folder, config_json=None):
    logger.info("CPU count: {}".format(mp.cpu_count()))
    f = Fhirndjson(config_json=config_json)
    filenames = []

    if os.path.isdir(folder):
        for filename in os.listdir(folder):
            if filename.endswith(".ndjson"):
                filenames.append(folder + "/" + filename)
    else:
        filenames.append(folder)

    with mp.Pool(mp.cpu_count()) as pool:
        list_of_dataframes = list(
            tqdm(
                pool.imap(f.process_file, filenames),
                total=len(filenames),
                desc="Processing NDJSON files",
            )
        )
    return pd.concat(list_of_dataframes)
