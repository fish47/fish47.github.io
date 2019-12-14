# -*- coding: utf-8 -*-

import math
import matplotlib.path as path
import matplotlib.pyplot as pyplot
import matplotlib.patches as patches


def _save_and_close_figure(fig, path):
    fig.savefig(path)
    pyplot.close(fig)


def _create_subplots(row, col, size_w, size_h):
    return pyplot.subplots(row, col,
                           sharex=True, sharey=True,
                           tight_layout=True,
                           figsize=(size_w, size_h))


def __is_straight_segment(sx, sy, c1x, c1y, c2x, c2y, ex, ey, factor):
    vec_se_x = sx - ex
    vec_se_y = sy - ey
    vec_c1s_x = c1x - sx
    vec_c1s_y = c1y - sy
    vec_c2s_x = c2x - sx
    vec_c2s_y = c2y - sy
    d1 = abs(vec_c1s_x * vec_se_y - vec_se_x * vec_c1s_y)
    d2 = abs(vec_c2s_x * vec_se_y - vec_se_x * vec_c2s_y)
    d3 = vec_se_x * vec_se_x + vec_se_y * vec_se_y
    d4 = d1 + d2
    return d4 * d4 < factor * d3


def __split_bezier_curve(sx, sy, c1x, c1y, c2x, c2y, endx, endy):
    def __mix(ax, ay, bx, by):
        return (ax + bx) * 0.5, (ay + by) * 0.5

    ax, ay = __mix(sx, sy, c1x, c1y)
    bx, by = __mix(c1x, c1y, c2x, c2y)
    cx, cy = __mix(c2x, c2y, endx, endy)
    dx, dy = __mix(ax, ay, bx, by)
    ex, ey = __mix(bx, by, cx, cy)
    fx, fy = __mix(dx, dy, ex, ey)
    l = (sx, sy, ax, ay, dx, dy, fx, fy)
    r = (fx, fy, ex, ey, cx, cy, endx, endy)
    return l, r


def __calc_bezier_segement_points(factor, sx, sy, c1x, c1y, c2x, c2y, ex, ey):
    def __push(stk, sx, sy, c1x, c1y, c2x, c2y, ex, ey):
        stk.append(sx)
        stk.append(sy)
        stk.append(c1x)
        stk.append(c1y)
        stk.append(c2x)
        stk.append(c2y)
        stk.append(ex)
        stk.append(ey)

    def __pop(stk):
        ey = stk.pop()
        ex = stk.pop()
        c2y = stk.pop()
        c2x = stk.pop()
        c1y = stk.pop()
        c1x = stk.pop()
        sy = stk.pop()
        sx = stk.pop()
        return sx, sy, c1x, c1y, c2x, c2y, ex, ey

    def __split(stk, sx, sy, c1x, c1y, c2x, c2y, ex, ey):
        l, r = __split_bezier_curve(sx, sy, c1x, c1y, c2x, c2y, ex, ey)
        __push(stk, *r)
        __push(stk, *l)

    stk = []
    points = []
    __push(stk, sx, sy, c1x, c1y, c2x, c2y, ex, ey)
    while (len(stk) > 0):
        sx, sy, c1x, c1y, c2x, c2y, ex, ey = __pop(stk)
        if __is_straight_segment(sx, sy, c1x, c1y, c2x, c2y, ex, ey, factor):
            if len(points) == 0:
                points.append((sx, sy))
            points.append((ex, ey))
        else:
            __split(stk, sx, sy, c1x, c1y, c2x, c2y, ex, ey)
    return points


def __plot_bezier_segment_points(axs, points, *args):
    axs.plot(*zip(*points), *args)


def __add_bezier_segments_patch(axs, verts, **kwargs):
    p = path.Path(verts)
    p = patches.PathPatch(p, fc='none', **kwargs)
    axs.add_patch(p)


def _plot_bezier(axs, factor, sx, sy, c1x, c1y, c2x, c2y, ex, ey):
    points = __calc_bezier_segement_points(
        factor, sx, sy, c1x, c1y, c2x, c2y, ex, ey)
    axs.plot((c1x, sx), (c1y, sy), 'k:')
    axs.plot((c2x, ex), (c2y, ey), 'k:')
    __add_bezier_segments_patch(axs, points, ec='r')
    __plot_bezier_segment_points(axs, points, 'r.')
    axs.plot((c1x, c2x), (c1y, c2y), 'bo')


def __add_bezier_curve_patch(axs, sx, sy, c1x, c1y, c2x, c2y, ex, ey, **kwargs):
    verts = (
        (sx, sy),
        (c1x, c1y),
        (c2x, c2y),
        (ex, ey),
        (0, 0),
    )
    codes = (
        path.Path.MOVETO,
        path.Path.CURVE4,
        path.Path.CURVE4,
        path.Path.CURVE4,
        path.Path.STOP,
    )
    p = path.Path(verts, codes)
    p = patches.PathPatch(p, fc='none', **kwargs)
    axs.add_patch(p)


def draw_bezier_segment_factor(size_w, size_h):
    def __plot(axs, limits, coords, factor):
        _plot_bezier(axs, factor, *coords)
        axs.set_title("factor = " + str(factor))
        axs.axis(limits)

    __limits = (100, 800, 350, 850)
    __bezier_coords = (
        200, 700,
        300, 450,
        600, 450,
        700, 700,
    )

    figure, axs_list = _create_subplots(1, 3, size_w, size_h)
    __plot(axs_list[0], __limits, __bezier_coords, 100)
    __plot(axs_list[1], __limits, __bezier_coords, 10)
    __plot(axs_list[2], __limits, __bezier_coords, 1)

    _save_and_close_figure(figure, "bezier_segment_factor.png")


def draw_bezier_curve_split(size_w, size_h):
    def __plot(axs, limits, sx, sy, c1x, c1y, c2x, c2y, ex, ey, **kwargs):
        axs.plot((c1x, sx), (c1y, sy), 'k:')
        axs.plot((c2x, ex), (c2y, ey), 'k:')
        axs.plot((c1x, c2x), (c1y, c2y), 'b.')
        axs.plot((sx, ex), (sy, ey), 'r.')
        __add_bezier_curve_patch(
            axs, sx, sy, c1x, c1y, c2x, c2y, ex, ey, **kwargs)
        axs.axis(limits)

    __limits = (100, 800, 350, 850)
    __bezier_coords = (
        200, 700,
        300, 450,
        600, 450,
        700, 700,
    )

    l, r = __split_bezier_curve(*__bezier_coords)

    figure, (axs1, axs2, axs3) = _create_subplots(1, 3, size_w, size_h)
    __plot(axs1, __limits, *__bezier_coords, ec='r')
    __plot(axs2, __limits, *l, ec='g')
    __add_bezier_curve_patch(axs2, *r, ec='k', ls=':')
    __plot(axs3, __limits, *r, ec='m')
    __add_bezier_curve_patch(axs3, *l, ec='k', ls=':')

    _save_and_close_figure(figure, "bezier_curve_split.png")


def draw_bezier_segment_distribution(size_w, size_h):
    __limits = (100, 800, 500, 900)
    __bezier_coords = (
        150, 750,
        250, 550,
        650, 850,
        750, 650,
    )
    figure, axs = _create_subplots(1, 1, size_w, size_h)
    _plot_bezier(axs, 3, *__bezier_coords)
    axs.axis(__limits)
    _save_and_close_figure(figure, "bezier_segment_distribution.png")


def __draw_arrow(axs, from_x, from_y, to_x, to_y):
    axs.annotate('', xy=(to_x, to_y),
                 xytext=(from_x, from_y),
                 arrowprops=dict(arrowstyle='->'))


def __draw_axis(axs, x, y, width, height, extend_x, extend_y):
    __draw_arrow(axs, x - extend_x, y, x + width, y)
    __draw_arrow(axs, x, y - extend_y, x, y + height)


def __add_arc_arrow_patch(axs, sx, sy, cx, cy, ex, ey):
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

    arrow_style = patches.ArrowStyle.Simple(head_width=4, head_length=6)
    arrow = patches.FancyArrowPatch(arrow_start, arrow_end,
                                    arrowstyle=arrow_style,
                                    connectionstyle=conn_style,
                                    color='k', lw=1)
    axs.add_patch(arrow)


def _annotate_text(axs, text, xy, xytext, style):
    if style:
        axs.plot(*xy, style)
    axs.annotate(text, xy=xy, xytext=xytext,
                 textcoords='offset points',
                 size='x-large')


def __get_step_point(from_xy, to_xy, step_len):
    vec_x = to_xy[0] - from_xy[0]
    vec_y = to_xy[1] - from_xy[1]
    vec_len = math.sqrt(vec_x * vec_x + vec_y * vec_y)
    factor = step_len / vec_len
    x = from_xy[0] + vec_x * factor
    y = from_xy[1] + vec_y * factor
    return x, y


def draw_cross_product_formula(size_w, size_h):
    __p0 = (0, 0)
    __pa = (4, 2)
    __pb = (2, 4)
    __axis_w = 6
    __axis_h = 6
    __axis_extend_x = 1
    __axis_extend_y = 1
    __arc_radius = 1
    __limits = (-4, 8, -5, 7)
    figure, axs = _create_subplots(1, 1, size_w, size_h)
    axs.axis(__limits)
    __draw_axis(axs, *__p0,
                __axis_w, __axis_h,
                __axis_extend_x, __axis_extend_y)

    _annotate_text(axs, '(0, 0)', __p0, (-44, -16), 'k.')

    __draw_arrow(axs, *__p0, *__pa)
    __draw_arrow(axs, *__p0, *__pb)

    __add_arc_arrow_patch(axs,
                          *__get_step_point(__p0, __pa, __arc_radius),
                          *__p0,
                          *__get_step_point(__p0, __pb, __arc_radius))

    _annotate_text(axs, r"$\theta$", __p0, (24, 20), None)
    _annotate_text(axs, r"$\vec A$ (x1, y1)", __pa, (-16, 4), None)
    _annotate_text(axs, r"$\vec B$ (x2, y2)", __pb, (-16, 2), None)

    _annotate_text(axs,
                   r"$\vec A \times \vec B = |\vec A| \cdot |\vec B| \cdot sin\theta$",
                   (-1, -2.5), (0, 0), None)
    _annotate_text(axs,
                   r"$\vec A \times \vec B = x1 \cdot y2 - x2 \cdot y1$",
                   (-1, -4), (0, 0), None)

    _save_and_close_figure(figure, "cross_product_formula.png")


def draw_cross_product_positive_negative(size_w, size_h):
    __p0 = (0, 0)
    __pa = (4, 2)
    __pb = (2, 4)
    __axis_w = 6
    __axis_h = 6
    __axis_extend_x = 1
    __axis_extend_y = 1
    __arc_radius = 3
    __limits = (-4, 8, -4, 8)

    def __plot(axs, pa, pb, op):
        axs.axis(__limits)
        __draw_axis(axs, *__p0,
                    __axis_w, __axis_h,
                    __axis_extend_x, __axis_extend_y)
        _annotate_text(axs, None, __p0, (0, 0), 'k.')

        __draw_arrow(axs, *__p0, *pa)
        __draw_arrow(axs, *__p0, *pb)

        __add_arc_arrow_patch(axs,
                              *__get_step_point(__p0, pa, __arc_radius),
                              *__p0,
                              *__get_step_point(__p0, pb, __arc_radius))

        _annotate_text(axs, r"$\vec A$", pa, (-4, 2), None)
        _annotate_text(axs, r"$\vec B$", pb, (-4, 2), None)
        _annotate_text(axs,
                       r"$\vec A \times \vec B$ " + op + " 0",
                       (-0.5, -2.5), (0, 0), None)

    figure, (axs1, axs2) = _create_subplots(1, 2, size_w, size_h)
    __plot(axs1, __pa, __pb, '>')
    __plot(axs2, __pb, __pa, '<')

    _save_and_close_figure(figure, "cross_product_positive_negative.png")


def __calc_parallelogram_point(p0, pa, pb):
    vec_x = pb[0] - p0[0]
    vec_y = pb[1] - p0[1]
    pc_x = pa[0] + vec_x
    pc_y = pa[1] + vec_y
    return pc_x, pc_y


def __calc_project_point(p0, pa, pb):
    vec_a_x = pa[0] - p0[0]
    vec_a_y = pa[1] - p0[1]
    vec_b_x = pb[0] - p0[0]
    vec_b_y = pb[1] - p0[1]
    cross_product = vec_b_x * vec_a_y - vec_a_x * vec_b_y
    len_b = math.sqrt(vec_b_x * vec_b_x + vec_b_y * vec_b_y)
    factor = cross_product / len_b / len_b
    vec_project_x = vec_b_y * factor
    vec_project_y = -vec_b_x * factor
    result_x = pa[0] + vec_project_x
    result_y = pa[1] + vec_project_y
    return result_x, result_y


def __add_parallelogram_patch(axs, p0, pa, pb, c):
    pc = __calc_parallelogram_point(p0, pa, pb)
    verts = (p0, pa, pc, pb)
    p = path.Path(verts)
    p = patches.PathPatch(p, color=c)
    axs.add_patch(p)


def __add_right_angle_patch(axs, top, rot, bottom, size):
    def __unit_vector(from_xy, to_xy):
        vec_x = to_xy[0] - from_xy[0]
        vec_y = to_xy[1] - from_xy[1]
        vec_len = math.sqrt(vec_x * vec_x + vec_y * vec_y)
        return vec_x / vec_len, vec_y / vec_len

    def __step(from_xy, vector, step):
        result_x = from_xy[0] + vector[0] * step
        result_y = from_xy[1] + vector[1] * step
        return result_x, result_y

    vec_top = __unit_vector(rot, top)
    vec_bottom = __unit_vector(rot, bottom)
    a = __step(rot, vec_top, size)
    c = __step(rot, vec_bottom, size)
    b = __step(c, vec_top, size)
    verts = (a, b, c)
    p = path.Path(verts)
    p = patches.PathPatch(p, fc='none', ec='k')
    axs.add_patch(p)


def draw_cross_product_parallelogram(size_w, size_h):
    __p0 = (0, 0)
    __pa = (4, 2)
    __pb = (2, 4)
    __axis_w = 6
    __axis_h = 6
    __axis_extend_x = 1
    __axis_extend_y = 1
    __arc_radius = 1.8
    __right_angle_size = 0.5
    __limits = (-4, 8, -5, 7)

    def __plot(axs, triangle_top, label, offset, formula1, formula2):
        axs.axis(__limits)
        __draw_axis(axs, *__p0,
                    __axis_w, __axis_h,
                    __axis_extend_x, __axis_extend_y)
        _annotate_text(axs, None, __p0, (0, 0), 'k.')

        __add_parallelogram_patch(axs, __p0, __pa, __pb, '#ffff0055')
        pc = __calc_parallelogram_point(__p0, __pa, __pb)
        axs.plot(*zip(__pa, pc), 'k:')
        axs.plot(*zip(__pb, pc), 'k:')

        prj = __calc_project_point(__p0,
                                   triangle_top,
                                   (triangle_top == __pa) and __pb or __pa)
        __draw_arrow(axs, *prj, *triangle_top)
        __add_right_angle_patch(axs,
                                triangle_top, prj,
                                __p0, __right_angle_size)

        __draw_arrow(axs, *__p0, *__pa)
        __draw_arrow(axs, *__p0, *__pb)

        __add_arc_arrow_patch(axs,
                              *__get_step_point(__p0, __pa, __arc_radius),
                              *__p0,
                              *__get_step_point(__p0, __pb, __arc_radius))

        _annotate_text(axs, r"$\theta$", __p0, (24, 20), None)
        _annotate_text(axs, r"$\vec A$", __pa, (-4, -20), None)
        _annotate_text(axs, r"$\vec B$", __pb, (-14, -2), None)
        _annotate_text(axs, r"$\vec " + label + r"$", prj, offset, None)

        _annotate_text(axs, r"$\vec A \times \vec B$" + formula1,
                       (-3, -2.5), (0, 0), None)
        _annotate_text(axs, formula2,
                       (-0.5, -4), (0, 0), None)

    figure, (axs1, axs2) = _create_subplots(1, 2, size_w, size_h)
    __plot(axs1, __pa, "C", (18, -6),
           r"$= |\vec B| \cdot |\vec A| \cdot sin\theta$",
           r"$= |\vec B| \cdot |\vec C|$")
    __plot(axs2, __pb, "D", (-4, 16),
           r"$= |\vec A| \cdot |\vec B | \cdot sin\theta$",
           r"$= |\vec A| \cdot |\vec D|$")

    _save_and_close_figure(figure, "cross_product_parallelogram.png")


def __do_draw_bezier_curve(axs, limits, sx, sy, c1x, c1y, c2x, c2y, ex, ey, label=True):
    axs.plot((c1x, sx), (c1y, sy), 'k:')
    axs.plot((c2x, ex), (c2y, ey), 'k:')
    axs.plot((c1x, c2x), (c1y, c2y), 'b.')
    axs.plot((sx, ex), (sy, ey), 'r.')
    __add_bezier_curve_patch(axs, sx, sy, c1x, c1y, c2x, c2y, ex, ey, ec='r')
    if label:
        _annotate_text(axs, 'A', (sx, sy), (-16, -4), None)
        _annotate_text(axs, 'C', (c1x, c1y), (0, -16), None)
        _annotate_text(axs, 'D', (c2x, c2y), (6, 4), None)
        _annotate_text(axs, 'B', (ex, ey), (8, -4), None)
    axs.axis(limits)


def draw_proof_bezier_curve(size_w, size_h):
    figure, axs = _create_subplots(1, 1, size_w, size_h)

    __limits = (100, 800, 450, 950)
    __bezier_coords = (
        200, 700,
        400, 550,
        500, 850,
        700, 700,
    )
    __do_draw_bezier_curve(axs, __limits, *__bezier_coords)
    _save_and_close_figure(figure, "proof_bezier_curve.png")


def __do_draw_proof_cross_product(size_w, size_h, label_curve, label_prj, label_d):
    def __center(p1, p2):
        x = (p1[0] + p2[0]) * 0.5
        y = (p1[1] + p2[1]) * 0.5
        return x, y

    figure, axs = _create_subplots(1, 1, size_w, size_h)

    __s = (200, 700)
    __c1 = (400, 550)
    __c2 = (500, 850)
    __e = (700, 700)
    __limits = (100, 800, 450, 950)
    __right_angle_size = 20
    __do_draw_bezier_curve(axs, __limits,
                           *__s, *__c1, *__c2, *__e,
                           label=label_curve)

    prj1 = __calc_project_point(__s, __c1, __e)
    prj2 = __calc_project_point(__e, __c2, __s)

    __add_right_angle_patch(axs, __c1, prj1, __s, __right_angle_size)
    __add_right_angle_patch(axs, __c2, prj2, __e, __right_angle_size)

    axs.plot(*zip(__s, __e), 'g:')
    axs.plot(*zip(__c1, prj1), 'm:')
    axs.plot(*zip(__c2, prj2), 'm:')

    if label_prj:
        _annotate_text(axs, 'E', prj1, (-4, 6), None)
        _annotate_text(axs, 'F', prj2, (-4, -16), None)

    if label_d:
        _annotate_text(axs, 'd1', __center(__c1, prj1), (4, 0), None)
        _annotate_text(axs, 'd2', __center(__c2, prj2), (-22, -4), None)

    return figure


def draw_proof_cross_product(size_w, size_h):
    figure = __do_draw_proof_cross_product(size_w, size_h, True, True, False)
    _save_and_close_figure(figure, "proof_cross_product.png")


def draw_proof_straight_curves(size_w, size_h):
    def __plot(axs, limits, angle_size, s, c1, c2, e):
        __do_draw_bezier_curve(axs, limits, *s, *c1, *c2, *e, label=False)
        prj1 = __calc_project_point(s, c1, e)
        prj2 = __calc_project_point(e, c2, s)
        axs.plot(*zip(s, e), 'g:')
        axs.plot(*zip(c1, prj1), 'm:')
        axs.plot(*zip(c2, prj2), 'm:')
        if angle_size > 0:
            __add_right_angle_patch(axs, c1, prj1, s, angle_size)
            __add_right_angle_patch(axs, c2, prj2, e, angle_size)

    __angle_size = 20
    __limits = (100, 800, 450, 950)

    figure, (axs1, axs2, axs3) = _create_subplots(1, 3, size_w, size_h)
    __plot(axs1, __limits, 0,
           (200, 700), (400, 700), (500, 700), (700, 700))
    __plot(axs2, __limits, __angle_size,
           (200, 700), (400, 650), (500, 750), (700, 700))
    __plot(axs3, __limits, __angle_size,
           (200, 700), (400, 600), (500, 800), (700, 700))

    _save_and_close_figure(figure, "proof_straight_curves.png")


draw_bezier_segment_factor(9, 3)
draw_bezier_segment_distribution(5, 4)
draw_bezier_curve_split(9, 3)
draw_cross_product_formula(5, 4)
draw_cross_product_positive_negative(6, 3)
draw_cross_product_parallelogram(6, 3)
draw_proof_bezier_curve(5, 4)
draw_proof_cross_product(5, 4)
draw_proof_straight_curves(9, 3)
