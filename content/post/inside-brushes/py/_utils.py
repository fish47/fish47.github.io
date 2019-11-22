# -*- coding: utf-8 -*-

import matplotlib.pyplot as pyplot

from _utils import *

__FIGURE_SIZE_MAP = {
    (1, 1): (6, 4),
    (1, 2): (8, 4),
    (1, 3): (8, 3),
    (2, 3): (8, 5),
    (2, 2): (6, 4),
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


def annotate_point(axs, text, xy, xytext, style):
    if style:
        axs.plot(*xy, style)
    axs.annotate(text, xy=xy, xytext=xytext,
                 textcoords='offset points',
                 size='x-large')
