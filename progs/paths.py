import os


# ===============================================================
#                      Repo/meta
# ===============================================================
def top_path():
    """Return path to top-level repo directory
    """
    path = os.path.join(os.path.dirname(__file__), '..')
    return path


def progenitor_sets_path():
    """Return path to top-level directory of progenitors
    """
    path = os.path.join(top_path(), 'progenitor_sets')
    return path


def config_filepath(series):
    """Return path to config file

    parameters
    ----------
    series : str
    """
    series = check_alias(series)
    filepath = os.path.join(top_path(), 'progs', 'config', f'{series}.ini')

    return filepath


def network_filepath(network):
    """Return path to table of given network

    parameters
    ----------
    network : str
    """
    filename = f'{network}.txt'
    filepath = os.path.join(top_path(), 'progs', 'networks', filename)

    return filepath


# ===============================================================
#                      Progenitors
# ===============================================================
def prog_filename(mass, series):
    """Return filename of progenitor

    parameters
    ----------
    mass : float/int
    series : str
    """
    def s16(mass_):
        return f's{mass_}_presn'

    def wh02(mass_):
        return f"s{mass_}_presn"

    filenames = {
        'sukhbold_2016': s16,
        "wh_02": wh02,
    }

    series = check_alias(series)

    if series in filenames:
        return filenames[series](mass)
    else:
        raise ValueError('Progenitor series not defined')


def prog_filepath(mass, series):
    """Return filepath to progenitor model

    parameters
    ----------
    mass : float/int
    series : str
    """
    filename = prog_filename(mass, series=series)
    filepath = os.path.join(series_path(series), filename)

    return filepath


def series_path(series):
    """Return path to progenitor series directory

    parameters
    ----------
    series : str
    """
    series = check_alias(series)
    series_dir = os.path.join(progenitor_sets_path(), series)

    return series_dir


def check_alias(series):
    """Return full name of series if alias used

    parameters
    ----------
    series : str
    """
    aliases = {
        's16': 'sukhbold_2016',
        's18': 'sukhbold_2018',
        'WH02': 'wh_02',
        'WH_02': "wh_02"
    }

    if series in aliases:
        return aliases[series]
    else:
        return series
