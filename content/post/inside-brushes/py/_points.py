# -*- coding: utf-8 -*-

import math

__RAW_POINTS = (
    445.7143, 474.3214,
    451.7143, 463.60715,
    455.00516, 456.75116,
    455.14285, 456.4643,
    460.2857, 446.64285,
    465.93192, 434.87994,
    470.57144, 425.2143,
    480.85715, 406.4643,
    487.90448, 395.73517,
    492.0, 389.5,
    505.7143, 371.64285,
    519.4286, 355.5714,
    525.6947, 349.42816,
    534.0, 341.2857,
    549.4286, 328.7857,
    566.5714, 317.17856,
    574.92163, 312.3946,
    583.7143, 307.35715,
    601.7143, 299.3214,
    618.8572, 293.0714,
    624.2272, 290.97375,
    632.5714, 287.7143,
    654.0, 280.5714,
    673.7143, 274.3214,
    680.0586, 272.73535,
    695.1429, 268.9643,
    710.9979, 265.96143,
    714.0, 265.39285,
    737.1429, 262.7143,
    759.4286, 261.8214,
    769.5384, 263.19504,
    779.1429, 264.5,
    799.7143, 268.0714,
    818.5714, 271.64285,
    825.2755, 273.11304,
    834.8572, 275.2143,
    845.1429, 278.7857,
    854.5714, 282.35715,
    854.7767, 282.4488,
    866.5714, 287.7143,
    877.7143, 295.75,
    893.1429, 308.25,
    895.8897, 310.90692,
    905.1429, 319.85715,
    912.0, 327.89285,
    917.1429, 334.14285,
    918.2503, 335.48865,
    922.2857, 342.17856,
    927.4286, 352.89285,
    930.0, 358.25,
    931.7143, 363.60715,
    935.1429, 377.89285,
    936.30786, 385.78088,
    938.5714, 401.10715,
    940.2857, 421.64285,
    939.4286, 442.17856,
    938.80554, 446.72153,
    936.8572, 460.92856,
    934.2857, 473.4286,
    930.6167, 486.42303,
    930.0, 488.60712,
    920.5714, 511.8214,
    910.2857, 533.25,
    900.0, 554.6786,
    899.2656, 556.20856,
    889.7143, 573.4286,
    876.8572, 590.3928,
    864.3092, 606.07776,
    864.0, 606.4643,
    851.1429, 619.8571,
    840.8572, 629.6786,
    834.40704, 635.27765,
    825.4286, 643.0714,
    810.0, 654.6786,
    809.12396, 655.33765,
    791.1429, 663.6071,
    772.2857, 668.9643,
    756.0, 671.6428,
    755.4262, 671.7372,
    746.5714, 672.5357,
    740.5714, 670.75,
    736.5019, 669.5388,
    734.5714, 668.9643,
    728.5714, 666.2857,
    721.7143, 662.7143,
    714.4865, 657.44403,
    713.1429, 656.4643,
    706.2857, 650.2143,
    702.0, 643.0714,
    698.1353, 633.67804,
    696.8572, 630.5714,
    691.7143, 608.25,
    690.0, 586.8214,
    690.05005, 586.2216,
    691.7143, 566.2857,
    695.1429, 543.0714,
    696.8572, 531.46423,
    701.1429, 521.6428,
    713.1429, 493.0714,
    724.2963, 471.12598,
    728.5714, 462.7143,
    743.1429, 435.92856,
    757.7143, 412.7143,
    765.88086, 402.93146,
    774.8572, 392.17856,
    791.1429, 370.75,
    810.0, 352.0,
    820.029, 342.97772,
    828.8572, 335.0357,
    848.5714, 320.75,
    868.2857, 308.25,
    876.572, 302.7572,
    887.1429, 295.75,
    906.0, 285.92856,
    926.5714, 277.89285,
    928.95013, 277.17014,
    947.1429, 271.64285,
    968.5714, 267.17856,
    990.0, 264.5,
    995.2607, 263.8424,
    1010.5714, 262.7143,
    1024.3286, 264.2497,
    1034.5714, 265.39285,
    1062.0, 270.75,
    1086.0, 277.0,
    1090.737, 278.38165,
    1107.4286, 283.25,
    1128.8572, 290.39285,
    1147.7144, 302.0,
    1153.9757, 306.1193,
    1164.0, 312.7143,
    1178.5714, 324.3214,
    1188.0, 331.4643,
    1190.9711, 334.3012,
    1198.2858, 341.2857,
    1212.8572, 357.35715,
    1224.0, 373.42856,
    1225.9598, 376.25522,
    1233.4286, 392.17856,
    1241.1428, 410.0357,
    1245.4286, 422.5357,
    1245.8712, 423.82663,
    1248.8572, 435.92856,
    1252.1136, 451.53268,
    1253.1428, 456.4643,
    1254.8572, 478.7857,
    1253.1428, 508.25,
    1252.6719, 511.3896,
    1248.8572, 536.8214,
    1242.0, 562.7143,
    1234.2858, 585.9286,
    1232.2556, 591.6383,
    1225.7144, 610.0357,
    1214.5714, 633.25,
    1200.8572, 653.7857,
    1200.2178, 654.7431,
    1186.2858, 675.2143,
    1170.8572, 695.75,
    1153.7144, 714.5,
    1152.8947, 715.3966,
    1136.5714, 734.1428,
    1117.7144, 751.1071,
    1100.5156, 764.7569,
    1099.7144, 765.3928,
    1081.7144, 777.8928,
    1064.5714, 788.6071,
    1056.0, 793.96423,
    1045.7144, 798.4286,
    1032.8992, 803.0717,
    1026.0, 805.5714,
    1002.8572, 810.0357,
    982.2857, 813.6071,
    965.1429, 814.5,
    964.1661, 814.5509,
    953.1429, 814.5,
    935.1429, 812.7143,
    925.2506, 810.9969,
    924.8572, 810.9286,
    915.4286, 808.25,
    906.8572, 802.0,
    900.61444, 796.21967,
    899.1429, 794.8571,
    891.4286, 786.8214,
    882.8572, 778.7857,
    877.57495, 770.5323,
    876.0, 768.0714,
    870.8572, 751.1071,
    869.1429, 740.3928,
    868.5646, 730.75464,
    868.2857, 726.1071,
    868.2857, 703.7857,
    868.2857, 703.3398,
    871.7143, 677.0,
    882.0, 647.5357,
    892.07007, 620.90814,
    893.1429, 618.0714,
    904.2857, 591.2857,
    918.0, 565.3928,
    930.46716, 545.1914,
    933.4286, 540.3928,
    949.7143, 518.0714,
    968.5714, 494.85712,
    980.519, 481.87067,
    988.2857, 473.4286,
    1007.1429, 453.7857,
    1028.5714, 436.8214,
    1041.1573, 426.44244,
    1049.1428, 419.85715,
    1072.2858, 404.67856,
    1093.7144, 392.17856,
    1105.2723, 386.62183,
    1116.0, 381.4643,
    1138.2858, 372.5357,
    1149.4287, 368.0714,
    1159.7144, 365.39285,
    1184.5714, 360.92856,
    1204.4474, 360.28156,
    1212.0, 360.0357,
    1239.4286, 360.92856,
    1263.4286, 363.60715,
    1279.4375, 365.90726,
    1288.2858, 367.17856,
    1308.8572, 375.2143,
    1326.8572, 384.14285,
    1336.8273, 390.07748,
    1344.8572, 394.85715,
    1362.0, 409.14285,
    1376.5714, 424.3214,
    1382.0748, 430.05417,
    1388.5714, 440.39285,
    1398.8572, 458.25,
    1407.4286, 476.10712,
    1409.6046, 483.87872,
    1413.4286, 497.5357,
    1417.7144, 518.9643,
    1420.2858, 540.3928,
    1420.9862, 546.2302,
    1421.1428, 563.6071,
    1420.634, 577.9194,
    1420.2858, 587.7143,
    1411.7144, 620.75,
    1402.2858, 652.8928,
    1397.0474, 667.8985,
    1392.0, 682.3571,
    1380.0, 712.7143,
    1365.4286, 741.2857,
    1349.1428, 769.8571,
    1330.2858, 798.4286,
    1310.5714, 828.7857,
    1302.6941, 840.1676,
    1284.0, 867.1786,
    1261.7144, 893.9643,
)


__PG_OFFSET = 16
__PG_DEFAULT = 1 << __PG_OFFSET
__PG_CONTROL = 1 << (__PG_OFFSET + 1)
__PG_BEZIER = 1 << (__PG_OFFSET + 2)

PF_PLOT = 1 | __PG_DEFAULT
PF_FILTER = (1 << 1) | __PG_DEFAULT
PF_AVERAGE = (1 << 2) | __PG_DEFAULT
PF_IN_OUT = (1 << 3) | __PG_CONTROL
PF_QUAD = (1 << 4) | __PG_CONTROL | __PG_BEZIER
PF_SEGMENT = (1 << 5) | __PG_CONTROL | __PG_BEZIER
PF_STAMP = (1 << 6) | __PG_DEFAULT


def __distance2(x1, y1, x2, y2):
    delta_x = x1 - x2
    delta_y = y1 - y2
    return delta_x * delta_x + delta_y * delta_y


def __distance(x1, y1, x2, y2):
    square = __distance2(x1, y1, x2, y2)
    return math.sqrt(square)


def __gen_pair(points):
    last_x = None
    for p in points:
        if last_x is None:
            last_x = p
        else:
            yield last_x, p
            last_x = None


def __gen_filter(points, slop):
    skipped = False
    last_x = None
    last_y = None
    slop2 = slop * slop
    for x, y in points:
        skipped = True
        if last_x is None or __distance2(x, y, last_x, last_y) > slop2:
            last_x = x
            last_y = y
            skipped = False
            yield x, y

    # 总是保留最后的点
    if skipped and x:
        yield x, y


def __gen_average(points):
    def __do_average(last_x, cur_x, next_x):
        mid_x = (last_x + next_x) * 0.5
        ret = (mid_x + cur_x) * 0.5
        return ret

    last_x = None
    last_y = None
    cur_x = None
    cur_x = None
    for x, y in points:
        if last_x is None:
            last_x = x
            last_y = y
        elif cur_x is None:
            cur_x = x
            cur_y = y
            yield last_x, last_y
        else:
            avg_x = __do_average(last_x, cur_x, x)
            avg_y = __do_average(last_y, cur_y, y)
            yield avg_x, avg_y
            last_x = cur_x
            last_y = cur_y
            cur_x = x
            cur_y = y
    if cur_x:
        yield cur_x, cur_y


def __gen_plot(points):
    x_list = []
    y_list = []
    for p in points:
        x_list.append(p[0])
        y_list.append(p[1])
    return x_list, y_list


#    [ a ]
# -> [ a ]
#    [ a, b ]
# -> [ a, b ]
#    [ a, b, c ]
# -> [ a, b_in, b, b_out, c ]
#    [ a, b, c, d ]
# -> [ a, b_in, b, b_out, c_in, c, c_out, c ]
def __gen_control(points):
    last_x = None
    last_y = None
    cur_x = None
    cur_y = None
    for x, y in points:
        if last_x is None:
            last_x = x
            last_y = y
            yield x, y
        elif cur_x is None:
            cur_x = x
            cur_y = y
        else:
            a_x = last_x
            a_y = last_y
            b_x = cur_x
            b_y = cur_y
            c_x = x
            c_y = y
            factor_in = 0
            factor_out = 0
            distance_ac = __distance(a_x, a_y, c_x, c_y)
            if distance_ac != 0:
                distance_ab = __distance(a_x, a_y, b_x, b_y)
                distance_bc = __distance(b_x, b_y, c_x, c_y)
                factor_in = distance_ab / distance_ac / 3
                factor_out = distance_bc / distance_ac / 3
            in_x = b_x + factor_in * (a_x - c_x)
            in_y = b_y + factor_in * (a_y - c_y)
            out_x = b_x + factor_out * (c_x - a_x)
            out_y = b_y + factor_out * (c_y - a_y)
            yield in_x, in_y
            yield b_x, b_y
            yield out_x, out_y
            last_x = cur_x
            last_y = cur_y
            cur_x = x
            cur_y = y
    if cur_x:
        yield cur_x, cur_y


#    [ a ]
# -> []
#    [ a, b ]
# -> []
#    [ a, b_in, b, b_out, c ]
# -> [ (b_in, b_out) ]
#    [ a, b_in, b, b_out, c_in, c, c_out, d ]
# -> [ (b_in, b_out), (c_in, c_out) ]
def __gen_in_out(points):
    skip_count = 2
    last_x = None
    last_y = None
    in_x = None
    in_y = None
    out_x = None
    out_y = None
    for x, y in points:
        if skip_count > 0:
            skip_count = skip_count - 1
        else:
            if in_x is None:
                skip_count = 1
                in_x = last_x
                in_y = last_y
            else:
                skip_count = 0
                out_x = last_x
                out_y = last_y
        if in_x and out_x:
            yield in_x, in_y, out_x, out_y
            in_x = None
            in_y = None
            out_x = None
            out_y = None
        last_x = x
        last_y = y


#     [ a ]
# ->  []
#     [ a, b ]
# ->  [ (a, a, b, b) ]
#     [ a, b_in, b, b_out, c ]
# ->  [ (a, b_in, b_in, b), (b, b_out, b_out, c) ]
#     [ a, b_in, b, b_out, c_in, c, c_out, d ]
# ->  [ (a, b_in, b_in, b), (b, b_out, c_in, c), (c, c_out, c_out, d) ]
def __gen_bezier(points):
    s_x = None
    s_y = None
    c1_x = None
    c1_y = None
    c2_x = None
    c2_y = None
    e_x = None
    e_y = None
    skip_count = 2
    for x, y in points:
        if skip_count > 0:
            skip_count = skip_count - 1
            if s_x is None:
                s_x = x
                s_y = y
            elif c1_x is None:
                c1_x = x
                c1_y = y
            elif c2_x is None:
                c2_x = x
                c2_y = y
        else:
            e_x = x
            e_y = y
            if c2_x is None:
                c2_x = x
                c2_y = y
            yield s_x, s_y, c1_x, c1_y, c2_x, c2_y, e_x, e_y
            skip_count = 2
            s_x = x
            s_y = y
            c1_x = None
            c1_y = None
            c2_x = None
            c2_y = None
            e_x = None
            e_y = None

    if s_x and c1_x:
        if c2_x:
            e_x = c2_x
            e_y = c2_y
        else:
            e_x = c1_x
            e_y = c1_y
            c1_x = s_x
            c1_y = s_y
            c2_x = e_x
            c2_y = e_y
        yield s_x, s_y, c1_x, c1_y, c2_x, c2_y, e_x, e_y


def __gen_quad(points):
    return points


def __gen_segment(points, split_factor):
    def __split(x1, y1, x2, y2):
        split_x = x1 + (x2 - x1) * 0.5
        split_y = y1 + (y2 - y1) * 0.5
        return split_x, split_y

    def __should_split(s_x, s_y, c1_x, c1_y, c2_x, c2_y, e_x, e_y, factor):
        d_x = e_x - s_x
        d_y = e_y - s_y
        d2 = math.fabs((c1_x - e_x) * d_y - (c1_y - e_y) * d_x)
        d3 = math.fabs((c2_x - e_x) * d_y - (c2_y - e_y) * d_x)
        return (d2 + d3) * (d2 + d3) > factor * (d_x * d_x + d_y * d_y)

    def __push(s, s_x, s_y, c1_x, c1_y, c2_x, c2_y, e_x, e_y):
        s.append(s_x)
        s.append(s_y)
        s.append(c1_x)
        s.append(c1_y)
        s.append(c2_x)
        s.append(c2_y)
        s.append(e_x)
        s.append(e_y)

    def __pop(s, factor):
        e_y = s.pop()
        e_x = s.pop()
        c2_y = s.pop()
        c2_x = s.pop()
        c1_y = s.pop()
        c1_x = s.pop()
        s_y = s.pop()
        s_x = s.pop()
        split = __should_split(s_x, s_y, c1_x, c1_y,
                               c2_x, c2_y, e_x, e_y, factor)
        return split, s_x, s_y, c1_x, c1_y, c2_x, c2_y, e_x, e_y

    yield_start = True
    stk = []
    for s_x, s_y, c1_x, c1_y, c2_x, c2_y, end_x, end_y in points:
        # 后面的迭代只返回线段结束位置
        if yield_start:
            yield s_x, s_y
            yield_start = False

        __push(stk, s_x, s_y, c1_x, c1_y, c2_x, c2_y, end_x, end_y)
        while len(stk) > 0:
            split, s_x, s_y, c1_x, c1_y, \
                c2_x, c2_y, end_x, end_y = __pop(stk, split_factor)
            if split:
                a_x, a_y = __split(s_x, s_y, c1_x, c1_y)
                b_x, b_y = __split(c1_x, c1_y, c2_x, c2_y)
                c_x, c_y = __split(c2_x, c2_y, end_x, end_y)
                d_x, d_y = __split(a_x, a_y, b_x, b_y)
                e_x, e_y = __split(b_x, b_y, c_x, c_y)
                f_x, f_y = __split(d_x, d_y, e_x, e_y)
                __push(stk,
                       f_x, f_y, e_x, e_y,
                       c_x, c_y, end_x, end_y)
                __push(stk,
                       s_x, s_y, a_x, a_y,
                       d_x, d_y, f_x, f_y)
            else:
                yield end_x, end_y


def __gen_stamp(points, step):
    last_stamp_x = None
    last_stamp_y = None
    used = 0
    remainder = 0
    for x, y in points:
        if last_stamp_x is None:
            last_stamp_x = x
            last_stamp_y = y
        else:
            distance = __distance(x, y, last_stamp_x, last_stamp_y)
            if distance > 0:
                vec_x = (x - last_stamp_x) / distance
                vec_y = (y - last_stamp_y) / distance
                step_x = vec_x * step
                step_y = vec_y * step
                stamp_x = last_stamp_x + vec_x * remainder
                stamp_y = last_stamp_y + vec_y * remainder
                used = remainder
                rad = math.atan2(vec_y, vec_x)
                while used <= distance:
                    yield stamp_x, stamp_y, rad
                    stamp_x = stamp_x + step_x
                    stamp_y = stamp_y + step_y
                    used = used + step
                remainder = used - distance
                last_stamp_x = x
                last_stamp_y = y
    if x is None and last_stamp_x is None:
        yield last_stamp_x, last_stamp_y, rad


def __test(flags, bits):
    return (flags & bits) == bits


def gen_points(flags, points=__RAW_POINTS,
               filter_step=100, segment_factor=10, stamp_step=30):
    gen = __gen_pair(points)
    if __test(flags, PF_FILTER):
        gen = __gen_filter(gen, filter_step)
    if __test(flags, PF_AVERAGE):
        gen = __gen_average(gen)
    if __test(flags, __PG_CONTROL):
        gen = __gen_control(gen)
    if __test(flags, PF_IN_OUT):
        gen = __gen_in_out(gen)
    if __test(flags, __PG_BEZIER):
        gen = __gen_bezier(gen)
    if __test(flags, PF_QUAD):
        gen = __gen_quad(gen)
    if __test(flags, PF_SEGMENT):
        gen = __gen_segment(gen, segment_factor)
    if __test(flags, PF_STAMP):
        gen = __gen_stamp(gen, stamp_step)
    if __test(flags, PF_PLOT):
        gen = __gen_plot(gen)
    return gen
