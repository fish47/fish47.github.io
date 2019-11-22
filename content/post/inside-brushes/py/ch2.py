# -*- coding: utf-8 -*-

from _utils import *
from _points import *


def __do_gen_points(bits):
    return gen_points(bits, filter_step=40)


def __plot_point(axs, text, xy, xytext):
    annotate_point(axs, text, xy, xytext, 'o')


def dash_from_to(axs, from_xy, to_xy):
    from_x, from_y = from_xy
    to_x, to_y = to_xy
    dx = to_x - from_x
    dy = to_y - from_y
    axs.arrow(from_x, from_y, dx, dy,
              ls=':', head_length=0, head_width=0)


def arrow_from_to(axs, from_xy, to_xy, style='<-'):
    axs.annotate('', xy=from_xy,
                 xytext=to_xy,
                 arrowprops=dict(arrowstyle=style))


def draw_compare_filter():
    bits = PF_PLOT
    figure, (axs1, axs2) = create_subplots(1, 2)
    axs1.set_title('Origin')
    axs1.plot(*__do_gen_points(bits), 'b.')
    axs2.set_title('Filtered')
    axs2.plot(*__do_gen_points(bits | PF_FILTER), 'r.')
    save_and_close_figure(figure, "compare_filter.png")


def draw_compare_averaged():
    bits = PF_FILTER | PF_PLOT
    figure, (axs1, axs2) = create_subplots(1, 2)
    axs1.set_title('Origin')
    axs1.plot(*__do_gen_points(bits), 'b.')
    axs2.set_title('Averaged')
    axs2.plot(*__do_gen_points(bits | PF_AVERAGE), 'r.')
    save_and_close_figure(figure, "compare_averaged.png")


def draw_compare_in_out_control():
    def __do_gen(bits):
        return gen_points(bits, filter_step=120)

    bits = PF_FILTER
    figure, (axs1, axs2) = create_subplots(1, 2)
    axs1.set_title('Origin')
    axs1.plot(*__do_gen(bits | PF_PLOT), 'b.')
    axs2.set_title('In-Out')
    axs2.plot(*__do_gen(bits | PF_PLOT), 'r.')
    for in_x, in_y, out_x, out_y in __do_gen(bits | PF_IN_OUT):
        arrow_from_to(axs2, (in_x, in_y), (out_x, out_y), style='<->')

    save_and_close_figure(figure, "compare_in_out_control.png")


def draw_plot_average():
    def __average(vec1, vec2):
        x = (vec1[0] + vec2[0]) / 2
        y = (vec1[1] + vec2[1]) / 2
        return (x, y)

    prev_p = (2, 4)
    curr_p = (3, 3)
    next_p = (4, 6)
    mid_p = __average(prev_p, next_p)
    result_p = __average(mid_p, curr_p)

    figure, axs = create_subplots(1, 1)
    __plot_point(axs, 'prev', prev_p, (-10, -20))
    __plot_point(axs, 'current', curr_p, (10, 0))
    __plot_point(axs, 'next', next_p, (-20, -20))
    __plot_point(axs, r'$mid=\frac{prev + next}{2}$',
                 mid_p, (10, -10))
    __plot_point(axs, r'$result=\frac{middle + current}{2}$',
                 result_p, (10, 5))

    dash_from_to(axs, prev_p, next_p)
    dash_from_to(axs, mid_p, curr_p)

    save_and_close_figure(figure, "plot_average.png")


def draw_plot_in_out_control():
    prev_p = (2, 4)
    curr_p = (3, 3)
    next_p = (4, 6)
    points = (
        *prev_p,
        *curr_p,
        *next_p,
    )
    in_x, in_y, out_x, out_y = next(gen_points(PF_IN_OUT, points=points))
    in_p = (in_x, in_y)
    out_p = (out_x, out_y)

    figure, axs = create_subplots(1, 1)
    __plot_point(axs, '(A) prev', prev_p, (-40, 10))
    __plot_point(axs, '(B) current', curr_p, (5, -15))
    __plot_point(axs, '(C) next', next_p, (-30, 10))
    __plot_point(axs,
                 r'$\vec{in}=\frac{1}{3}\times\frac{|AB|}{|AC|}\times\vec{CA}$',
                 in_p, (-95, -20))
    __plot_point(axs,
                 r'$\vec{out}=\frac{1}{3}\times\frac{|BC|}{|AC|}\times\vec{AC}$',
                 out_p, (-10, -25))

    dash_from_to(axs, prev_p, next_p)
    dash_from_to(axs, prev_p, curr_p)
    dash_from_to(axs, curr_p, next_p)

    arrow_from_to(axs, curr_p, in_p)
    arrow_from_to(axs, curr_p, out_p)

    l, r = axs.get_xlim()
    t, b = axs.get_ylim()
    axs.set_xlim(l - 0.5, r + 0.8)
    axs.set_ylim(t - 0.5, b + 0.5)

    save_and_close_figure(figure, "plot_in_out_control.png")


draw_compare_filter()
draw_compare_averaged()
draw_compare_in_out_control()
draw_plot_average()
draw_plot_in_out_control()
