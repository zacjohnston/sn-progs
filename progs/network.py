import numpy as np
import pandas as pd

# progs
from . import paths
from . import configuration

"""
Functions for handling nuclear network information
"""


def load_network(set_name,
                 config=None):
    """Load network profile from file
    
    Returns : pd.DataFrame
    
    parameters
    ----------
    set_name : str
    config : {}
    """
    config = configuration.check_config(config=config, set_name=set_name)
    network_name = config['network']['name']

    filepath = paths.network_filepath(network_name)
    network = pd.read_csv(filepath, delim_whitespace=True)

    return network


def get_sums(composition, network):
    """Calculate summed quantities from isotope composition
    
    Returns : pd.DataFrame
    
    parameters
    ----------
    composition : pd.DataFrame
        profile of isotope mass fractions
    network : pd.DataFrame
        profile of isotopes to sum over, as returned by load_net().
        isotope labels must match the column names in `composition`
    """
    sums_dict = {}
    n_zones = len(composition)

    for key in ['sumx', 'sumy', 'ye']:
        sums_dict[key] = np.zeros(n_zones)

    for _, isotope in network.iterrows():
        x = np.array(composition[isotope['isotope']], dtype=float)

        sums_dict['sumx'] += x
        sums_dict['sumy'] += x / isotope['A']
        sums_dict['ye'] += x * (isotope['Z'] / isotope['A'])

    sums_dict['abar'] = 1 / sums_dict['sumy']
    sums = pd.DataFrame(sums_dict)

    return sums
