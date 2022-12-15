import os
import numpy as np
import pandas as pd
from astropy import units
from astropy import constants as const

# progs
from . import paths
from . import configuration

g_to_msun = units.g.to(units.M_sun)
cm_to_1k_km = units.cm.to(1e3 * units.km)


# =======================================================
#                 Files
# =======================================================
def find_progs(progset_name,
               config=None):
    """Find all available progenitor models in a set

    Returns : [str]
        list of ZAMS masses

    parameters
    ----------
    progset_name : str
    config : {}
    """
    config = configuration.check_config(config=config, progset_name=progset_name)
    path = paths.set_path(progset_name)

    progs = []
    filelist = os.listdir(path)

    for filename in filelist:
        if config['load']['match_str'] in filename:
            zams = filename.strip(config['load']['strip'])
            progs += [zams]

    progs = sorted(progs, key=float)

    return progs


# =======================================================
#                 Loading tables
# =======================================================
def load_profile(zams,
                 progset_name,
                 config=None):
    """Load progenitor model from file
    
    Returns : pd.DataFrame
    
    parameters
    ----------
    zams : str
    progset_name : str
    config : {}
    """
    config = configuration.check_config(config=config, progset_name=progset_name)
    raw = load_raw_table(zams, progset_name, config=config)
    profile = pd.DataFrame()

    for key, idx in config['columns'].items():
        profile[key] = pd.to_numeric(raw[idx], errors='ignore')

    profile['mass'] = profile['mass'] * g_to_msun

    add_derived_columns(profile, config=config)

    return profile


def load_raw_table(zams,
                   progset_name,
                   config=None):
    """Load unformatted progenitor model from file

    Returns : pd.DataFrame
    
    parameters
    ----------
    zams : str
    progset_name : str
    config : {}
    """
    config = configuration.check_config(config, progset_name=progset_name)
    filepath = paths.prog_filepath(zams, progset_name)

    delim_whitespace = config['load']['delim_whitespace']
    skiprows = config['load']['skiprows']
    missing_char = config['load']['missing_char']

    raw = pd.read_csv(filepath,
                      delim_whitespace=delim_whitespace,
                      skiprows=skiprows,
                      header=None)

    raw = raw.replace(missing_char, 0.0)

    return raw


# =======================================================
#                  Derived columns
# =======================================================
def add_derived_columns(profile,
                        config):
    """Add derived column variables to profile
    
    parameters
    ----------
    profile : pd.DataFrame
    config : {}
    """
    derived_cols = config['load']['derived_columns']

    if 'compactness' in derived_cols:
        add_compactness(profile)
    if 'luminosity' in derived_cols:
        add_luminosity(profile)
    if 'iron_group' in derived_cols:
        add_iron_group(profile, isotopes=config['network']['iron_group'])


def add_compactness(profile):
    """Add compactness column to profile

    parameters
    ----------
    profile : pd.DataFrame
    """
    if ('radius' not in profile) or ('mass' not in profile):
        raise ValueError(f'Need radius and mass columns to calculate compactness')

    profile['compactness'] = profile['mass'] / (profile['radius'] * cm_to_1k_km)


def add_luminosity(profile):
    """Add blackbody luminosity column to profile

    parameters
    ----------
    profile : pd.DataFrame
    """
    if ('radius' not in profile) or ('temperature' not in profile):
        raise ValueError(f'Need radius and temperature columns to calculate luminosity')

    sb = const.sigma_sb.cgs.value
    radius = profile['radius']
    temp = profile['temperature']

    profile['luminosity'] = 4 * np.pi * sb * radius**2 * temp**4


def add_iron_group(profile, isotopes):
    """Add Combined iron group composition to profile

    parameters
    ----------
    profile : pd.DataFrame
    isotopes : [str]
        iron group isotopes to combine
    """
    iron = np.zeros(len(profile))

    for iso in isotopes:
        iron += profile[iso]

    profile['iron_group'] = iron
