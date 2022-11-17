import pandas as pd

# progs
from . import paths
from . import configuration


def load_prog(mass,
              series,
              config=None):
    """Load progenitor model from file

    parameters
    ----------
    mass : float/int
    series : str
    config : dict
    """
    config = configuration.check_config(config, series=series)
    raw = load_raw(mass, series, config=config)
    prog = pd.DataFrame()

    for key, idx in config['columns'].items():
        prog[key] = pd.to_numeric(raw[idx], errors='ignore')

    return prog


def load_raw(mass,
             series,
             config=None):
    """Load raw progenitor model from file

    parameters
    ----------
    mass : float/int
    series : str
    config : dict
    """
    config = configuration.check_config(config, series=series)
    filepath = paths.prog_filepath(mass, series)

    delim_whitespace = config['load']['delim_whitespace']
    skiprows = config['load']['skiprows']
    missing_char = config['load']['missing_char']

    raw = pd.read_csv(filepath,
                      delim_whitespace=delim_whitespace,
                      skiprows=skiprows,
                      header=None)

    return raw.replace(missing_char, 0.0)


