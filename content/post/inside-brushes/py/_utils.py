# -*- coding: utf-8 -*-

import matplotlib.pyplot as pyplot

from _utils import *

__FIGURE_SIZE_MAP = {
    (1, 1): (6, 4),
    (1, 2): (8, 4),
}


def create_subplots(row, col, *args, **kwargs):
    size = __FIGURE_SIZE_MAP[(row, col)]
    return pyplot.subplots(row, col,
                           sharex=True, sharey=True,
                           tight_layout=True, figsize=size,
                           *args, **kwargs)


def save_and_close_figure(fig, path):
    fig.savefig(path)
    pyplot.close(fig)
