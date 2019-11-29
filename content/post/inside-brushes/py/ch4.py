# -*- coding: utf-8 -*-

import math

import matplotlib.path as path
import matplotlib.pyplot as pyplot
import matplotlib.patches as patches
import matplotlib.transforms as transforms

from _utils import *
from _points import *


def draw_rotate_upright_compare():
    def __do_add_rect_patch(axs, x, y, rad, size, color, rotate):
        center_x = x - size / 2
        center_y = y - size / 2
        pos = (center_x, center_y)
        rect = patches.Rectangle(pos, size, size, fill=False, ec=color)
        if rotate:
            trans = transforms.Affine2D()\
                .translate(-x, -y)\
                .rotate(rad)\
                .translate(x, y)
            rect.set_transform(trans + axs.transData)
        axs.add_patch(rect)

    def __add_upright_rect(axs, _, x, y, rad, size, color):
        __do_add_rect_patch(axs, x, y, rad, size, color, False)

    def __add_self_rotate_rect(axs, first, x, y, rad, size, c, radius, llen, lw, lc):
        __do_add_rect_patch(axs, x, y, rad, size, c, True)
        if first:
            from_x = x + radius
            from_y = y
            to_x = x + radius * math.cos(rad)
            to_y = y + radius * math.sin(rad)
            axs.plot((x, x + llen), (y, y), lc + '-')
            add_arc_arrow_patch(axs, lc,
                                from_x, from_y,
                                x, y, to_x, to_y,
                                no_head=True, lw=lw)

    __points = (
        1, 4,
        2.5, 2.5,
        6, 4.5,
        7, 7,
    )
    __limits = (0, 8, 1, 9)
    __stamp_step = 0.8
    __stamp_size = 0.8
    __arc_radius = 0.6
    __line_length = 1
    __arc_line_width = 1.5
    __stamp_color = 'g'
    __line_color = 'b'

    x_list = []
    y_list = []
    figure, (axs1, axs2) = create_subplots(1, 2)
    axs1.axis(__limits)
    axs2.axis(__limits)
    iter_stamp_rects(axs1,
                     gen_points(PF_STAMP,
                                points=__points,
                                stamp_step=__stamp_step),
                     __add_upright_rect,
                     __stamp_size, __stamp_color)
    iter_stamp_rects(axs2,
                     gen_points(PF_STAMP,
                                points=__points,
                                stamp_step=__stamp_step),
                     __add_self_rotate_rect,
                     __stamp_size, __stamp_color,
                     __arc_radius, __line_length,
                     __arc_line_width, __line_color)

    axs1.plot(*gen_points(PF_PLOT, points=__points), 'r-')
    axs1.plot(*gen_points(PF_STAMP | PF_PLOT,
                          points=__points, stamp_step=__stamp_step),
              'r.')
    axs2.plot(*gen_points(PF_PLOT, points=__points), 'r-')
    axs2.plot(*gen_points(PF_STAMP | PF_PLOT,
                          points=__points, stamp_step=__stamp_step),
              'r.')

    save_and_close_figure(figure, "rotate_upright_compare.png")


def __apply(transform, xy):
    np_array = transform.transform(xy)
    return tuple(np_array)


def __arrow(axs, from_x, from_y, to_x, to_y, style='->'):
    axs.annotate('', xy=(to_x, to_y),
                 xytext=(from_x, from_y),
                 arrowprops=dict(arrowstyle=style))


def draw_rotate_calc_steps():
    __limits = (0, 20, 0, 20)
    __rect_x = 4
    __rect_y = 5
    __rect_w = 10
    __rect_h = 10
    __rotate_rad = math.pi / 6
    __rect_c_x = __rect_x + __rect_w / 2
    __rect_c_y = __rect_y + __rect_h / 2
    __transform = transforms.Affine2D()\
        .rotate_around(__rect_c_x, __rect_c_y, __rotate_rad)

    __anno_origin_rect = (
        ('P0', (0, -20), (__rect_x, __rect_y)),
        ('P1', (0, -20), (__rect_x + __rect_w,  __rect_y)),
        ('P2', (0,  10), (__rect_x + __rect_h,  __rect_y + __rect_h)),
        ('P3', (0,  10), (__rect_x,  __rect_y + __rect_h)),
    )

    __anno_rotated_rect = (
        ('P0\'', (-5, -20), __apply(__transform, __anno_origin_rect[0][2])),
        ('P1\'', (-5, -20), __apply(__transform, __anno_origin_rect[1][2])),
        ('P2\'', (0,   10), __apply(__transform, __anno_origin_rect[2][2])),
        ('P3\'', (-10, 10), __apply(__transform, __anno_origin_rect[3][2])),
    )

    __anno_half_sizes = (
        ('W/2', (-12, -18), (__rect_c_x + __rect_w / 4, __rect_c_y)),
        ('H/2', (5, -2), (__rect_c_x, __rect_c_y + __rect_h / 4)),
    )

    __anno_center = (
        ('C', (-15, -15), (__rect_c_x, __rect_c_y)),
    )

    def __plot_annos(axs, annos, style):
        for text, offset, xy in annos:
            annotate_point(axs, text, xy, offset, style)

    def __plot_polygon(axs, annos, **style):
        codes = []
        verts = []
        for _, __, xy in annos:
            code = len(codes) == 0 \
                and path.Path.MOVETO \
                or path.Path.LINETO
            codes.append(code)
            verts.append(xy)
        codes.append(path.Path.CLOSEPOLY)
        verts.append((0, 0))
        p = path.Path(verts, codes)
        patch = patches.PathPatch(p, fill=False, **style)
        axs.add_patch(patch)

    def __plot_rotate_angle(axs, cx, cy, w, rad, c1, c2, c3):
        def __calc(x, y, r, rad):
            bx = x + r
            by = y
            rx = x + r * math.cos(rad)
            ry = y + r * math.sin(rad)
            return bx, by, rx, ry

        bx, by, rx, ry = __calc(cx, cy, w / 2, rad)
        axs.plot((cx, bx), (cy, by), c1 + '-')
        axs.plot((cx, rx), (cy, ry), c2 + '-')

        arc_sx, arc_sy, arc_ex, arc_ey = __calc(cx, cy, w * 0.35, rad)
        add_arc_arrow_patch(axs, c3, arc_sx, arc_sy, cx, cy, arc_ex, arc_ey)

    def __plot_size_mark(axs, cx, cy, w, h):
        __arrow(axs, cx, cy, cx + w / 2, cy, style='<->')
        __arrow(axs, cx, cy, cx, cy + h / 2, style='<->')

    figure, (axs1, axs2, axs3) = create_subplots(1, 3)
    axs1.axis(__limits)
    axs2.axis(__limits)
    axs3.axis(__limits)

    __plot_annos(axs1, __anno_center, 'ro')

    __plot_annos(axs2, __anno_center, 'ro')
    __plot_annos(axs2, __anno_origin_rect, 'bo')
    __plot_polygon(axs2, __anno_origin_rect, ls='-', ec='b')
    __plot_size_mark(axs2, __rect_c_x, __rect_c_y, __rect_w, __rect_h)
    __plot_annos(axs2, __anno_half_sizes, None)

    __plot_annos(axs3, __anno_origin_rect, 'bo')
    __plot_annos(axs3, __anno_rotated_rect, 'go')
    __plot_polygon(axs3, __anno_origin_rect, ls='-', ec='b')
    __plot_polygon(axs3, __anno_rotated_rect, ls=':', ec='g')
    __plot_rotate_angle(axs3, __rect_c_x, __rect_c_y, __rect_w,
                        __rotate_rad, 'b', 'g', 'r')
    __plot_annos(axs3, __anno_center, 'ro')

    save_and_close_figure(figure, "rotate_calc_steps.png")


def draw_rotate_matrix_steps():
    __limits = (-5, 20, -5, 20)
    __axis_vec_x = (-2, 10)
    __axis_vec_y = (-2, 10)
    __origin_xy = (0, 0)
    __rotate_xy = (10, 10)
    __p2_origin_xy = (15, 15)
    __p2_rotated_xy = __apply(
        transforms.Affine2D()
        .rotate_around(*__rotate_xy, math.pi / 6),
        __p2_origin_xy)

    __anno_c = ('C', __rotate_xy, (-16, 6), 'go')
    __anno_p2 = ('P2', __p2_origin_xy, (0, 10), 'bo')
    __anno_p2_r = ('P2\'', __p2_rotated_xy, (0, 8), 'ro')

    def __plot_axis(axis, xy, vec_x, vec_y):
        axis_x_from = (xy[0] + vec_x[0], xy[1])
        axis_x_to = (xy[1] + vec_x[1], xy[1])
        axis_y_from = (xy[0], xy[1] + vec_y[0])
        axis_y_to = (xy[0], xy[1] + vec_y[1])
        __arrow(axis, *axis_x_from, *axis_x_to)
        __arrow(axis, *axis_y_from, *axis_y_to)

    def __plot_anno(axis, anno):
        annotate_point(axis, *anno)

    def __plot_rotate(axis, p, c, pr):
        axis.plot(*zip(c, p), 'k:')
        axis.plot(*zip(c, pr), 'k:')
        add_arc_arrow_patch(axis, 'k', *p, *c, *pr)

    figure, (axs1, axs2, axs3, axs4) = create_subplots(1, 4)
    axs1.axis(__limits)
    axs2.axis(__limits)
    axs3.axis(__limits)
    axs4.axis(__limits)

    __plot_axis(axs1, __origin_xy, __axis_vec_x, __axis_vec_y)
    __plot_anno(axs1, __anno_c)
    __plot_anno(axs1, __anno_p2)
    axs1.set_title('origin')

    __plot_axis(axs2, __rotate_xy, __axis_vec_x, __axis_vec_y)
    __plot_anno(axs2, __anno_c)
    __plot_anno(axs2, __anno_p2)
    axs2.set_title('translate(x, y)')

    __plot_axis(axs3, __rotate_xy, __axis_vec_x, __axis_vec_y)
    __plot_rotate(axs3, __p2_origin_xy, __rotate_xy, __p2_rotated_xy)
    __plot_anno(axs3, __anno_c)
    __plot_anno(axs3, __anno_p2)
    __plot_anno(axs3, __anno_p2_r)
    axs3.set_title('rotate(angle)')

    __plot_axis(axs4, __origin_xy, __axis_vec_x, __axis_vec_y)
    __plot_anno(axs4, __anno_c)
    __plot_anno(axs4, __anno_p2)
    __plot_anno(axs4, __anno_p2_r)
    axs4.set_title('translate(-x, -y)')

    save_and_close_figure(figure, "rotate_matrix_steps.png")


def __add_path_patch(axs, annos, **styles):
    codes = []
    verts = []
    p0 = None
    p1 = None
    p2 = None
    for _, p, __ in annos:
        p0 = p1
        p1 = p2
        p2 = p
        if p0 and p1:
            codes.append(path.Path.LINETO)
            codes.append(path.Path.LINETO)
            codes.append(path.Path.MOVETO)
            verts.append(p2)
            verts.append(p0)
            verts.append(p2)
        elif p1 and p2:
            codes.append(path.Path.MOVETO)
            codes.append(path.Path.LINETO)
            verts.append(p1)
            verts.append(p2)

    if len(verts) and len(codes):
        p = path.Path(verts, codes)
        patch = patches.PathPatch(p, **styles)
        axs.add_patch(patch)


def __plot_triangles(axs, limits, annos):
    axs.axis(limits)
    __add_path_patch(axs, annos, fill=False, ec='b')
    for anno in annos:
        annotate_point(axs, *anno, 'ro')


def draw_triangles_linestripe():
    __limits = (0, 12, 0, 10)
    __annos = (
        ('0', (2, 3), (-16, -6)),
        ('1', (4, 6), (-4, 10)),
        ('2', (5, 2), (-4, -18)),
        ('3', (7, 8), (-4, 8)),
        ('4', (8, 3), (0, -18)),
        ('5', (10, 7), (8, -2)),
    )
    figure, axs_list = create_subplots(2, 3)
    __plot_triangles(axs_list[0][0], __limits, __annos[:1])
    __plot_triangles(axs_list[0][1], __limits, __annos[:2])
    __plot_triangles(axs_list[0][2], __limits, __annos[:3])
    __plot_triangles(axs_list[1][0], __limits, __annos[:4])
    __plot_triangles(axs_list[1][1], __limits, __annos[:5])
    __plot_triangles(axs_list[1][2], __limits, __annos[:6])

    save_and_close_figure(figure, "triangles_linestripe.png")


def draw_triangles_degenerate_overview():
    __limits = (0, 24, 0, 24)
    __annos = (
        ('a0', (2, 6), (-24, -14)),
        ('b0', (8, 6), (6, -14)),
        ('c0', (2, 12), (-24, 0)),
        ('d00', (8, 12), (6, 4)),
        ('d01', (8, 12), (6, -14)),

        ('a10', (6, 16), (-32, -14)),
        ('a11', (6, 16), (-32, 4)),
        ('b1', (12, 16), (6, -14)),
        ('c1', (6, 22), (-24, 0)),
        ('d10', (12, 22), (6, 4)),
        ('d11', (12, 22), (6, -14)),

        ('a20', (16, 10), (-32, -14)),
        ('a21', (16, 10), (-32, 4)),
        ('b2', (22, 10), (6, -14)),
        ('c2', (16, 16), (-24, 0)),
        ('d2', (22, 16), (6, 0)),
    )

    figure, axs = create_subplots(1, 1)
    __plot_triangles(axs, __limits, __annos)

    save_and_close_figure(figure, "degenerate_overview.png")


def draw_triangles_degenerate_mechanism():
    def __move(annos, name, dx, dy, text_x, text_y):
        for i in range(len(annos)):
            text, p, offset = annos[i]
            if text == name:
                annos[i] = (text,
                            (p[0] + dx, p[1] + dy),
                            (text_x, text_y))
                break

    __limits = (0, 24, 0, 24)
    __annos = (
        ('a0', (4, 2), (-22, -10)),
        ('b0', (13, 2), (6, -10)),
        ('c0', (4, 9), (-22, 0)),
        ('d00', (13, 9), (6, 4)),
        ('d01', (13, 9), (6, -14)),
        ('a10', (10, 14), (-32, -14)),
        ('a11', (10, 14), (-32, 4)),
        ('b1', (19, 14), (6, -10)),
        ('c1', (10, 21), (-22, 0)),
        ('d1', (19, 21), (6, 0))
    )

    annos1 = list(__annos)
    __move(annos1, 'a11', 0, 0, -32, -10)
    __move(annos1, 'b1', 0, 0, 6, -10)
    __move(annos1, 'd00', 0, 0, 6, 0)
    __move(annos1, 'd01', -4, 0, -14, -18)
    __move(annos1, 'a10', 4, 0, -16, 6)

    annos2 = list(annos1)
    __move(annos2, 'd01', 2, 0, -14, -18)
    __move(annos2, 'a10', -2, 0, -8, 6)

    figure, (axs1, axs2, axs3) = create_subplots(1, 3)

    __add_path_patch(axs1, annos1[3:7], fc='g')
    __plot_triangles(axs1, __limits, annos1)

    __add_path_patch(axs2, annos2[3:7], fc='g')
    __plot_triangles(axs2, __limits, annos2)

    __plot_triangles(axs3, __limits, __annos)

    save_and_close_figure(figure, "triangles_degenerate_mechanism.png")


draw_rotate_upright_compare()
draw_rotate_calc_steps()
draw_rotate_matrix_steps()
draw_triangles_linestripe()
draw_triangles_degenerate_overview()
draw_triangles_degenerate_mechanism()
