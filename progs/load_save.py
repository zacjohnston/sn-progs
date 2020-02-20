import numpy as np
import pandas as pd

# progs
from . import paths
from . import configuration


def load_prog(mass, series, verbose=True):
    """Load progenitor model from file

    parameters
    ----------
    mass : float/int
    series : str
    verbose : bool
    """
    config = configuration.load_config(series, verbose)
    raw = load_raw(mass, series, config=config, verbose=verbose)
    prog = pd.DataFrame()

    for key, idx in config['columns'].items():
        prog[key] = raw[idx]

    return prog


def load_raw(mass, series, config=None, verbose=True):
    """Load raw progenitor model from file

    parameters
    ----------
    mass : float/int
    series : str
    config : dict
    verbose : bool
    """
    conf = configuration.check_config(config, series=series, verbose=verbose)
    filepath = paths.prog_filepath(mass, series)

    raw = pd.read_csv(filepath, delim_whitespace=conf['load']['delim_whitespace'],
                      skiprows=conf['load']['skiprows'], header=None)

    return raw


