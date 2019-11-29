# -*- coding: utf-8 -*-

import numpy

import matplotlib.patches as patches
import matplotlib.transforms as transforms

from matplotlib.path import Path
from matplotlib.image import BboxImage

from _utils import *
from _points import *


def draw_intro_filter():
    bits = PF_PLOT
    figure, axs = create_subplots(1, 1)
    axs.plot(*gen_points(bits), 'b.', label='origin')
    axs.plot(*gen_points(bits | PF_FILTER), 'ro', label='filtered')
    axs.legend()
    save_and_close_figure(figure, "intro_filter.png")


def draw_intro_averaged():
    bits = PF_PLOT | PF_FILTER
    figure, axs = create_subplots(1, 1)
    axs.plot(*gen_points(bits), 'b.-', label='filtered')
    axs.plot(*gen_points(bits | PF_AVERAGE), 'r.:', label='averaged')
    axs.legend()
    save_and_close_figure(figure, "intro_averaged.png")


def _draw_in_out_pairs(axs, bits, color, label):
    one_shot_label = label
    for in_x, in_y, out_x, out_y in gen_points(bits | PF_IN_OUT):
        axs.plot((in_x, out_x), (in_y, out_y), color, label=one_shot_label)
        one_shot_label = None


def _draw_bezier_curves(axs, bits, color):
    codes = []
    verts = []
    for s_x, s_y, c1_x, c1_y, c2_x, c2_y, e_x, e_y in gen_points(bits):
        codes.append(Path.MOVETO)
        codes.append(Path.CURVE4)
        codes.append(Path.CURVE4)
        codes.append(Path.CURVE4)
        verts.append((s_x, s_y))
        verts.append((c1_x, c1_y))
        verts.append((c2_x, c2_y))
        verts.append((e_x, e_y))
    codes.append(Path.STOP)
    verts.append((0, 0))
    p = Path(tuple(verts), tuple(codes))
    p = patches.PathPatch(p, facecolor='none', edgecolor=color)
    axs.add_patch(p)


def __draw_rect(axs, _, x, y, rad, size, color):
    center_x = x - size / 2
    center_y = y - size / 2
    pos = (center_x, center_y)
    rect = patches.Rectangle(pos, size, size, fill=False, ec=color)
    if rad and rad != 0:
        trans = transforms.Affine2D()\
            .translate(-x, -y)\
            .rotate(rad)\
            .translate(x, y)
        rect.set_transform(trans + axs.transData)
    axs.add_patch(rect)


def __draw_mosaic(axs, _, x, y, rad, size, data):
    half_size = size / 2
    trans = transforms.Affine2D()\
        .translate(-half_size, -half_size)\
        .translate(-x, -y)\
        .rotate(rad)\
        .translate(x, y)
    rect = (x, x + size, y, y + size)
    img = axs.imshow(data, cmap='gray', origin='lower', extent=rect)
    img.set_transform(trans + axs.transData)


def _draw_stamp_rects(axs, points, size, color):
    iter_stamp_rects(axs, points, __draw_rect, size, color)


def _draw_stamp_textures(axs, points, size):
    data = numpy.random.rand(16, 16)
    iter_stamp_rects(axs, points, __draw_mosaic, size, data)


def draw_intro_control_points():
    bits = PF_FILTER | PF_AVERAGE
    figure, axs = create_subplots(1, 1)
    axs.plot(*gen_points(bits | PF_PLOT), 'b.:', label='averaged')
    _draw_in_out_pairs(axs, bits | PF_IN_OUT, 'r.-', 'control')
    axs.legend()
    save_and_close_figure(figure, "intro_control_points.png")


def draw_intro_control_curves():
    bits = PF_FILTER | PF_AVERAGE
    figure, axs = create_subplots(1, 1)
    axs.plot(*gen_points(bits | PF_PLOT), 'b.', label='averaged')
    _draw_in_out_pairs(axs, bits | PF_IN_OUT, 'r.-', 'control')
    _draw_bezier_curves(axs, bits | PF_QUAD, 'g')
    axs.legend()
    save_and_close_figure(figure, "intro_control_curves.png")


def draw_intro_segment_points():
    bits = PF_FILTER | PF_AVERAGE
    figure, axs = create_subplots(1, 1)
    axs.plot(*gen_points(bits | PF_SEGMENT | PF_PLOT), 'r.', label='segment')
    _draw_bezier_curves(axs, bits | PF_QUAD, 'g')
    save_and_close_figure(figure, "intro_segment_points.png")


def draw_intro_stamp_points():
    bits = PF_FILTER | PF_AVERAGE | PF_SEGMENT | PF_STAMP | PF_PLOT
    figure, axs = create_subplots(1, 1)
    axs.plot(*gen_points(bits), 'r.')
    save_and_close_figure(figure, "intro_stamp_points.png")


def draw_intro_stamp_rects():
    bits = PF_FILTER | PF_AVERAGE | PF_SEGMENT | PF_STAMP
    figure, axs = create_subplots(1, 1)
    axs.plot(*gen_points(bits | PF_PLOT), 'r.')
    _draw_stamp_rects(axs, gen_points(bits), 30, 'g')
    save_and_close_figure(figure, "intro_stamp_rects.png")


def draw_intro_stamp_fill():
    bits = PF_FILTER | PF_AVERAGE | PF_SEGMENT | PF_STAMP
    figure, axs = create_subplots(1, 1)
    axs.plot(*gen_points(bits | PF_PLOT), 'r.')
    _draw_stamp_textures(axs, gen_points(bits), 30)
    save_and_close_figure(figure, "intro_stamp_textures.png")


draw_intro_filter()
draw_intro_averaged()
draw_intro_control_points()
draw_intro_control_curves()
draw_intro_segment_points()
draw_intro_stamp_points()
draw_intro_stamp_rects()
draw_intro_stamp_fill()
