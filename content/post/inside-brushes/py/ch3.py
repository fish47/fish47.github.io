# -*- coding: utf-8 -*-

import math

import matplotlib.path as path
import matplotlib.patches as patches
import matplotlib.gridspec as gridspec

from _utils import *
from _points import *


def __center(points, idx1, idx2):
    t = 0.5
    x = points[idx1][0] * t + points[idx2][0] * (1 - t)
    y = points[idx1][1] * t + points[idx2][1] * (1 - t)
    return (x, y)


__AXS_LIMITS = (1, 8, 3, 7)

__POINTS_ORIGIN = (
    (2, 5),
    (3, 4),
    (6, 4),
    (7, 6),
)
__POINTS_SPLIT_1 = (
    __center(__POINTS_ORIGIN, 0, 1),
    __center(__POINTS_ORIGIN, 1, 2),
    __center(__POINTS_ORIGIN, 2, 3),
)
__POINTS_SPLIT_2 = (
    __center(__POINTS_SPLIT_1, 0, 1),
    __center(__POINTS_SPLIT_1, 1, 2),
)
__POINTS_SPLIT_3 = (
    __center(__POINTS_SPLIT_2, 0, 1),
)

__ANNO_ORIGIN = (
    (__POINTS_ORIGIN[0], (-15, 10), 'start'),
    (__POINTS_ORIGIN[1], (-5, -20), 'out'),
    (__POINTS_ORIGIN[2], (-5, -20), 'in'),
    (__POINTS_ORIGIN[3], (-15, 10), 'end'),
)
__ANNO_SPLIT_1 = (
    (__POINTS_SPLIT_1[0], (-15, -15),  'A'),
    (__POINTS_SPLIT_1[1], (0, -20),  'B'),
    (__POINTS_SPLIT_1[2], (10,  -10),  'C'),
)
__ANNO_SPLIT_2 = (
    (__POINTS_SPLIT_2[0], (-5, -20),  'D'),
    (__POINTS_SPLIT_2[1], (8, -16),  'E'),
)
__ANNO_SPLIT_3 = (
    (__POINTS_SPLIT_3[0], (0, -20), 'F'),
)


def __create_path(s, c1, c2, e):
    codes = (
        path.Path.MOVETO,
        path.Path.CURVE4,
        path.Path.CURVE4,
        path.Path.CURVE4,
        path.Path.STOP,
    )
    verts = (
        s, c1, c2, e, (0, 0)
    )
    return path.Path(verts, codes)


def draw_bezier_divide_step():
    def __line_to(axs, annotations, line_idx1, line_idx2, color):
        from_p, _, __ = annotations[line_idx1]
        to_p, _, __ = annotations[line_idx2]
        axs.plot(*zip(from_p, to_p), color + ':')

    def __plot(axs, split_anno, annotations, line_idx1, line_idx2, color1, color2):
        axs.axis(__AXS_LIMITS)
        for p, offset, text in annotations:
            annotate_point(axs, text, p, offset, color1 + 'o')
        __line_to(axs, annotations, line_idx1, line_idx2, color1)

        p, offset, text = split_anno
        annotate_point(axs, text, p, offset, color2 + 'o')

    figure, axs_list = create_subplots(2, 3)
    __plot(axs_list[0][0], __ANNO_SPLIT_1[0], __ANNO_ORIGIN, 0, 1, 'b', 'r')
    __plot(axs_list[0][1], __ANNO_SPLIT_1[1], __ANNO_ORIGIN, 1, 2, 'b', 'r')
    __plot(axs_list[0][2], __ANNO_SPLIT_1[2], __ANNO_ORIGIN, 2, 3, 'b', 'r')
    __plot(axs_list[1][0], __ANNO_SPLIT_2[0], __ANNO_SPLIT_1, 0, 1, 'r', 'g')
    __plot(axs_list[1][1], __ANNO_SPLIT_2[1], __ANNO_SPLIT_1, 1, 2, 'r', 'g')
    __plot(axs_list[1][2], __ANNO_SPLIT_3[0], __ANNO_SPLIT_2, 0, 1, 'g', 'm')

    save_and_close_figure(figure, "bezier_divide_step.png")


def draw_bezier_split_overview():
    def __plot_curve(axs, path_l, path_r, line_l, line_r, title):
        path_props = {
            'fc': 'none',
            'edgecolor': 'k',
        }
        axs.axis(__AXS_LIMITS)
        axs.set_title(title)
        axs.add_patch(patches.PathPatch(path_l, **path_props, ls=line_l))
        axs.add_patch(patches.PathPatch(path_r, **path_props, ls=line_r))

    def __plot_controls(axs, style, *annos):
        x_list = []
        y_list = []
        for p, offset, text in annos:
            x_list.append(p[0])
            y_list.append(p[1])
            annotate_point(axs, text, p, offset, None)
        axs.plot(x_list, y_list, style)

    figure, (axs1, axs2, axs3) = create_subplots(1, 3)
    path_left = __create_path(__POINTS_ORIGIN[0], __POINTS_SPLIT_1[0],
                              __POINTS_SPLIT_2[0], __POINTS_SPLIT_3[0])
    path_right = __create_path(__POINTS_SPLIT_3[0], __POINTS_SPLIT_2[1],
                               __POINTS_SPLIT_1[2], __POINTS_ORIGIN[3])

    __plot_curve(axs1, path_left, path_right, None, None, 'Origin')
    __plot_curve(axs2, path_left, path_right, None, ':', 'Segment1')
    __plot_curve(axs3, path_left, path_right, ':', None, 'Segment2')

    __plot_controls(axs1, 'bo:', *__ANNO_ORIGIN)
    __plot_controls(axs2, 'ro:',
                    __ANNO_ORIGIN[0], __ANNO_SPLIT_1[0],
                    __ANNO_SPLIT_2[0], __ANNO_SPLIT_3[0])
    __plot_controls(axs3, 'go:',
                    __ANNO_SPLIT_3[0], __ANNO_SPLIT_2[1],
                    __ANNO_SPLIT_1[2], __ANNO_ORIGIN[3])

    save_and_close_figure(figure, "bezier_split_overview.png")


def draw_bezier_split_factor():
    def __plot(axs, factor):
        __points = (
            200, 700,
            300, 450,
            600, 450,
            700, 700,
        )
        __limits = (100, 800, 300, 800)
        flags = PF_SEGMENT | PF_PLOT
        axs.axis(__limits)
        axs.set_title('Factor = ' + str(factor))
        axs.plot(*gen_points(flags, points=__points,
                             segment_factor=factor), 'r.-')

    figure, axs_list = create_subplots(2, 2)
    __plot(axs_list[0][0], 4000)
    __plot(axs_list[0][1], 2500)
    __plot(axs_list[1][0], 800)
    __plot(axs_list[1][1], 40)

    save_and_close_figure(figure, "bezier_split_factor.png")


def draw_bezier_subcurves():
    def __slice_raw(flatten, idx):
        return flatten[idx:idx + 2]

    def __slice_in_out(flatten, idx1, idx2):
        return flatten[idx1][idx2:idx2 + 2]

    __limits = (0, 10, 2, 9.5)
    __points_raw = (
        1, 4.5,
        3.2, 3.5,
        6.4, 4,
        8, 6,
        6, 8,
    )
    flatten = tuple(gen_points(PF_IN_OUT, points=__points_raw))

    __anno_origin = (
        (__slice_raw(__points_raw, 0), (-10, -20), 'P0'),
        (__slice_raw(__points_raw, 2), (-10, -20), 'P1'),
        (__slice_raw(__points_raw, 4), (5, -15), 'P2'),
        (__slice_raw(__points_raw, 6), (8, -5), 'P3'),
        (__slice_raw(__points_raw, 8), (5, 5), 'P4'),
    )
    __anno_in_out = (
        (__slice_in_out(flatten, 0, 0), (0, 0), 'P1-in'),
        (__slice_in_out(flatten, 0, 2), (-15, -20), 'P1-out'),
        (__slice_in_out(flatten, 1, 0), (5, -15), 'P2-in'),
        (__slice_in_out(flatten, 1, 2), (8, -8), 'P2-out'),
        (__slice_in_out(flatten, 2, 0), (6, -8), 'P3-in'),
        (__slice_in_out(flatten, 2, 2), (0, 0), 'P3-out'),
    )
    __anno_curve1 = (
        __anno_origin[0],
        __anno_origin[0],
        __anno_in_out[0],
        __anno_origin[1],
    )
    __anno_curve2 = (
        __anno_origin[1],
        __anno_in_out[1],
        __anno_in_out[2],
        __anno_origin[2],
    )
    __anno_curve3 = (
        __anno_origin[2],
        __anno_in_out[3],
        __anno_in_out[4],
        __anno_origin[3],
    )
    __anno_curve4 = (
        __anno_origin[3],
        __anno_in_out[5],
        __anno_origin[4],
        __anno_origin[4],
    )

    def __do_annotate_point(axs, anno):
        p, offset, text = anno
        annotate_point(axs, text, p, offset, None)

    def __plot_annotations(axs, style, *annos):
        x_list = []
        y_list = []
        last_anno = None
        for anno in annos:
            if anno != last_anno:
                last_anno = anno
                p, offset, text = anno
                x_list.append(p[0])
                y_list.append(p[1])
                annotate_point(axs, text, p, offset, None)
        axs.plot(x_list, y_list, style)

    def __plot_curves(axs, ls, *annos):
        axs.axis(__limits)
        for i in range(0, len(annos), 4):
            s = annos[i]
            c1 = annos[i + 1]
            c2 = annos[i + 2]
            e = annos[i + 3]
            p = __create_path(s[0], c1[0], c2[0], e[0])
            axs.add_patch(patches.PathPatch(
                p, edgecolor='k', fc='none', ls=ls))

    figure, (axs1, axs2) = create_subplots(1, 2)

    __plot_curves(axs1, '-', *__anno_curve2)
    __plot_curves(axs1, ':', *__anno_curve1, *__anno_curve3, *__anno_curve4)
    __plot_annotations(axs1, 'k.', *__anno_origin)
    __plot_annotations(axs1, 'r.:', *__anno_curve2)

    __plot_curves(axs2, '-', *__anno_curve3)
    __plot_curves(axs2, ':', *__anno_curve1, *__anno_curve2, *__anno_curve4)
    __plot_annotations(axs2, 'k.', *__anno_origin)
    __plot_annotations(axs2, 'b.:', *__anno_curve3)

    save_and_close_figure(figure, "bezier_subcurves.png")


def __get_vec_len(vec_x, vec_y):
    return math.sqrt(vec_x * vec_x + vec_y * vec_y)


def __do_draw_remainder(points, limits, stamp_step, file_name):
    def __eq(a, b):
        return abs(a - b) < 0.0001

    def __is_parallel(vec_x1, vec_y1, vec_x2, vec_y2):
        return __eq(vec_x1, vec_x2) and __eq(vec_y1, vec_y2)

    def __is_in_segment(ax, ay, bx, by, cx, cy):
        x1 = ax - bx
        y1 = ay - by
        x2 = cx - bx
        y2 = cy - by
        dot_product = x1 * y2 - x2 * y1
        cross_product = x1 * x2 + y1 * y2
        return __eq(dot_product, 0) and cross_product < 0

    def __iterate_collapsed_points(points, last_x, last_y, adv_x, adv_y, next_x, next_y):
        found = False
        abort = False
        idx = 0
        step = 2
        end_idx = len(points) - step
        while idx <= end_idx and not abort:
            x = points[idx]
            y = points[idx + 1]
            if not found:
                if __is_in_segment(last_x, last_y, x, y, adv_x, adv_y):
                    found = True
            else:
                if idx == end_idx or __is_in_segment(last_x, last_y, next_x, next_y, x, y):
                    abort = True
            if found:
                yield x, y, abort
            idx = idx + step

    def __draw_bent_points_and_arcs(axs, step, style,
                                    last_x, last_y, adv_x, adv_y, next_x, next_y):
        vec_x = (adv_x - last_x)
        vec_y = (adv_y - last_y)
        vec_len = __get_vec_len(vec_x, vec_y)
        vec_unit_x = vec_x / vec_len
        vec_unit_y = vec_y / vec_len

        x_list = [last_x]
        y_list = [last_y]
        arc_args = []
        rot_x = None
        rot_y = None
        it_adv_x = None
        it_adv_y = None
        last_seg_x = None
        last_seg_y = None
        for x, y, is_last in __iterate_collapsed_points(points,
                                                        last_x, last_y,
                                                        adv_x, adv_y,
                                                        next_x, next_y):
            if rot_x is None:
                rot_x = x
                rot_y = y
                it_adv_x = x
                it_adv_y = y
            else:
                end_point = is_last and (next_x, next_y) or (x, y)
                delta_x = end_point[0] - last_seg_x
                delta_y = end_point[1] - last_seg_y
                step_len = __get_vec_len(delta_x, delta_y)
                it_adv_x = it_adv_x + vec_unit_x * step_len
                it_adv_y = it_adv_y + vec_unit_y * step_len
                x_list.append(it_adv_x)
                y_list.append(it_adv_y)
                arc_args.append((it_adv_x, it_adv_y, rot_x, rot_y, *end_point))

            last_seg_x = x
            last_seg_y = y

        axs.plot(x_list, y_list, style)
        for args in arc_args:
            add_arc_arrow_patch(axs, 'k', *args)

    def __find_last_bend_point(points, step):
        last_vec_x = None
        last_vec_y = None
        last_x = None
        last_y = None
        for x, y, _ in gen_points(PF_STAMP, points=points, stamp_step=step):
            if last_x:
                vec_x = x - last_x
                vec_y = y - last_y
                if last_vec_x and not __is_parallel(vec_x, vec_y, last_vec_x, last_vec_y):
                    last_vec_len = __get_vec_len(last_vec_x, last_vec_y)
                    advance_x = last_x + step * last_vec_x / last_vec_len
                    advance_y = last_y + step * last_vec_y / last_vec_len
                    return last_x, last_y, advance_x, advance_y, x, y
                last_vec_x = vec_x
                last_vec_y = vec_y
            last_x = x
            last_y = y

    figure, axs = create_subplots(1, 1)
    axs.axis(limits)

    bend_data = __find_last_bend_point(points, stamp_step)
    if bend_data:
        __draw_bent_points_and_arcs(axs, stamp_step, 'b.:', *bend_data)

    axs.plot(*gen_points(PF_PLOT, points=points), 'go-')
    axs.plot(*gen_points(PF_STAMP | PF_PLOT,
                         points=points, stamp_step=stamp_step), 'r.')

    save_and_close_figure(figure, file_name)


def draw_stamp_remainder():
    __stamp_step = 10
    __limits = (10, 100, 30, 80)
    __points = (
        20, 70,
        50, 40,
        90, 50,
    )
    __do_draw_remainder(__points, __limits, __stamp_step,
                        "stamp_remainder.png")


def draw_stamp_short_segments():
    __stamp_step = 20
    __limits = (10, 100, 25, 75)
    __points = (
        20, 70,
        50, 40,
        57, 40,
        62, 42,
        90, 60,
    )
    __do_draw_remainder(__points, __limits, __stamp_step,
                        "stamp_short_segments.png")


draw_bezier_divide_step()
draw_bezier_split_overview()
draw_bezier_split_factor()
draw_bezier_subcurves()
draw_stamp_remainder()
draw_stamp_short_segments()
