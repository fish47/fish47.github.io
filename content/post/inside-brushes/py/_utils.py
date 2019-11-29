# -*- coding: utf-8 -*-

import math
import matplotlib.pyplot as pyplot
import matplotlib.patches as patches

from _utils import *

__FIGURE_SIZE_MAP = {
    (1, 1): (6, 4),
    (1, 2): (8, 4),
    (1, 3): (8, 3),
    (1, 4): (10, 3),
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


def iter_stamp_rects(axs, points, fn, *args):
    def __eq(a, b):
        return abs(a - b) < 0.0001

    # 插入图形后，视图位置会莫名奇妙地改变，先备份一下
    x_lim = axs.get_xlim()
    y_lim = axs.get_ylim()

    last_rad = None
    for x, y, rad in points:
        changed = last_rad is None or not __eq(last_rad, rad)
        fn(axs, changed, x, y, rad, *args)
        last_rad = rad

    # 恢复视图位置
    axs.set_xlim(x_lim)
    axs.set_ylim(y_lim)


def add_arc_arrow_patch(axs, c, sx, sy, cx, cy, ex, ey, no_head=False, lw=None):
    __rad_factor = 0.5
    vec_from_x = sx - cx
    vec_from_y = sy - cy
    vec_to_x = ex - cx
    vec_to_y = ey - cy
    rad_from = math.atan2(vec_from_y, vec_from_x)
    rad_to = math.atan2(vec_to_y, vec_to_x)
    rad_delta = (rad_to - rad_from) * __rad_factor

    arrow_start = (sx, sy)
    arrow_end = (ex, ey)
    conn_style = patches.ConnectionStyle.Arc3(rad=rad_delta)
    conn_style.connect(arrow_start, arrow_end)

    arrow_style = no_head\
        and patches.ArrowStyle.Curve()\
        or patches.ArrowStyle.Simple(head_width=4, head_length=6)
    arrow = patches.FancyArrowPatch(arrow_start, arrow_end,
                                    arrowstyle=arrow_style,
                                    connectionstyle=conn_style,
                                    color=c, lw=lw)
    axs.add_patch(arrow)
