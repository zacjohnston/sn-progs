import numpy as np

# progs
from . import paths
from . import load_save
from . import configuration
from . import network
from . import plotting
from . import tools

"""
Class for handling a given progenitor model
"""


class Prog:
    def __init__(self, mass, series, verbose=True):
        """Object representing a single progenitor model

        parameters
        ----------
        mass : float/int
            Stellar mass (in Msun) of progenitor model.
            Precision needs to match the file label
                e.g. mass=12.1 for 's12.1_presn',
                     mass=60 for 's60_presn'
        series : str
            Name of progenitor series/set, e.g. 'sukhbold_2016'.
            Shorthand aliases may be defined, e.g. 's16' for 'sukhbold_2016'.
        verbose : bool


        attributes
        ----------
        mass : int or float
        series : str
        verbose : bool
        filename : str
        filepath : str
            Path to raw progenitor file
        config : dict
            Progenitor-specific parameters loaded from 'config/[series].ini'
        network : [str]
            table of network isotopes used
        table : pd.DataFrame
            Main table of radial profile parameters, including composition
        composition : pd.DataFrame
            subset of table containing only network species abundances (mass fraction)
        sums : dict
            summed composition quantities (e.g. sumx, sumy, ye)
        """
        self.mass = mass
        self.series = paths.check_alias(series)
        self.verbose = verbose

        self.filename = paths.prog_filename(mass, series=series)
        self.filepath = paths.prog_filepath(mass, series=series)
        self.config = configuration.load_config(series, verbose)

        self.table = load_save.load_prog(mass, series, config=self.config,
                                         verbose=verbose)

        network_name = self.config['network']['name']
        self.network = network.load_network(network_name)
        self.composition = self.table[self.network.isotope]
        self.sums = network.get_sums(self.composition, self.network)

    # =======================================================
    #                      Plotting
    # =======================================================
    # def plot_multi(self, y_vars, x_var='r', y_scale=None, x_scale=None,
    #                max_cols=2, sub_figsize=(6, 5), trans=True, legend=False):
    #     """Plot one or more profile variables
    #
    #     parameters
    #     ----------
    #     y_vars : str or [str]
    #         column(s) from self.table to plot on y-axis
    #     x_var : str
    #         variable to plot on x-axis
    #     y_scale : {'log', 'linear'}
    #     x_scale : {'log', 'linear'}
    #     legend : bool
    #     max_cols : bool
    #     sub_figsize : tuple
    #     trans : bool
    #     """
    #     y_vars = tools.ensure_sequence(y_vars)
    #     n_var = len(y_vars)
    #     fig, ax = plotting.setup_subplots(n_var, max_cols=max_cols,
    #                                       sub_figsize=sub_figsize, squeeze=False)
    #
    #     for i, y_var in enumerate(y_vars):
    #         row = int(np.floor(i / max_cols))
    #         col = i % max_cols
    #
    #         self.plot_profile(chk, y_var=y_var, x_var=x_var, y_scale=y_scale,
    #                           x_scale=x_scale, ax=ax[row, col], trans=trans,
    #                           legend=legend if i == 0 else False)
    #     return fig
    #
    # def plot(self, y_var, x_var='r', y_scale=None, x_scale=None,
    #          ax=None, legend=False, trans=True, title=True,
    #          ylims=None, xlims=None, figsize=(8, 6), label=None,
    #          linestyle='-', marker=''):
    #     """Plot given profile variable
    #
    #     parameters
    #     ----------
    #     y_var : str
    #         variable to plot on y-axis (from Simulation.profile)
    #     x_var : str
    #         variable to plot on x-axis
    #     y_scale : {'log', 'linear'}
    #     x_scale : {'log', 'linear'}
    #     ax : Axes
    #     legend : bool
    #     trans : bool
    #     title : bool
    #     ylims : [min, max]
    #     xlims : [min, max]
    #     figsize : [width, height]
    #     label : str
    #     linestyle : str
    #     marker : str
    #     """
    #     fig, ax = plotting.check_ax(ax=ax, figsize=figsize)
    #
    #     for i in chk:
    #         profile = self.profiles.sel(chk=i)
    #         y = profile[y_var]
    #
    #         ax.plot(profile[x_var], y, ls=linestyle, marker=marker, label=label)
    #         self._plot_trans_line(x_var, y=y, ax=ax, chk=i, trans=trans)
    #
    #     if legend:
    #         ax.legend()
    #
    #     return fig
