from matplotlib import pyplot as plt
from random import randint
from math import atan2
from time import time

def create_points(ct, min=0, max=50):
    return [[randint(min, max), randint(min, max)] for _ in range(ct)]

def scatter_plot(coords, convex_hull=None):
    xs, ys = zip(*coords)
    plt.scatter(xs, ys)

    if convex_hull is not None:
        for i in range(1, len(convex_hull) + 1):
            if i == len(convex_hull):
                i = 0  # wrap
            c0 = convex_hull[i - 1]
            c1 = convex_hull[i]
            plt.plot((c0[0], c1[0]), (c0[1], c1[1]), 'r')

    plt.show()

def polar_angle(p0, p1=None):
    if p1 is None:
        p1 = anchor
    y_span = p0[1] - p1[1]
    x_span = p0[0] - p1[0]
    return atan2(y_span, x_span)

def det(p1, p2, p3):
    return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])

def jarvis_march(points, show_progress=False):
    global anchor
    min_idx = points.index(min(points, key=lambda p: (p[1], p[0])))
    anchor = points[min_idx]

    hull = [anchor]
    while True:
        endpoint = points[0]
        for candidate in points[1:]:
            if endpoint == anchor or det(anchor, endpoint, candidate) > 0:
                endpoint = candidate

        if endpoint == hull[0]:
            break
        else:
            hull.append(endpoint)
            if show_progress:
                scatter_plot(points, hull)

        anchor = endpoint

    return hull

sizes = [10, 100, 1000, 10000, 100000]
for s in sizes:
    tot = 0.0
    for _ in range(3):
        pts = create_points(s, 0, max(sizes) * 10)
        t0 = time()
        hull = jarvis_march(pts, False)
        tot += (time() - t0)
    print("size %d time: %0.5f" % (s, tot / 3.0))

pts = create_points(10)
print("Points:", pts)
hull = jarvis_march(pts, True)
print("Hull:", hull)
scatter_plot(pts, hull)
