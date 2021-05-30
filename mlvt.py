import builtins
from inspect import getframeinfo, stack
import plotille
import numpy as np
import re


class Line:
    def __init__(self, width, height, color="green", accumulate=False):
        self.width = width
        self.height = height
        self.accumulate = accumulate
        self.data = None
        self.color = color
        if self.accumulate is True:
            self.data = np.array([])
        elif self.accumulate:
            self.data = np.zeros(self.accumulate)
            self.cur_len = 0
            self.cur_start = 0

    def update(self, data):
        if self.accumulate is True:
            self.data = np.append(self.data, data)
        elif self.accumulate:
            if self.cur_len == self.accumulate:
                self.data = np.roll(self.data, -1)
                self.cur_start += 1
                self.data[-1] = data
            else:
                self.data[self.cur_len] = data
            if self.cur_len < self.accumulate:
                self.cur_len += 1
        else:
            self.data = data

    def show(self):
        fig = plotille.Figure()
        fig.width = self.width
        fig.height = self.height
        if self.accumulate:
            fig.x_label = "iters"
        if self.data is None:
            return ""
        d = self.data
        start = 0
        if self.accumulate is not True and self.accumulate:
            d = self.data[: self.cur_len]
            start = self.cur_start
        if d.size <= 1:
            return ""
        fig.set_x_limits(min_=start, max_=len(d) + start)
        fig.set_y_limits(min_=float(np.min(d)), max_=float(np.max(d)))
        fig.plot(np.arange(len(d)) + start, d, lc=self.color)
        return fig.show()

    def __str__(self):
        return self.show()


class Histogram:
    def __init__(self, width, height, color=None, bins=None):
        self.height = height
        self.width = width
        self.data = None
        self.color = color
        self.bins = bins
        if self.bins == None:
          self.bins = self.width

    def update(self, data):
        self.data = data

    def show(self):
        if self.data is None:
            return ""
        return plotille.histogram(
            self.data,
            height=self.height,
            bins=self.bins,
            width=self.width,
            lc=self.color,
        )

    def __str__(self):
        return self.show()


def pool(X, ksize):
    m, n = X.shape[:2]
    ky, kx = ksize

    ny = m // ky
    nx = n // kx
    X_pad = X[: ny * ky, : nx * kx, ...]

    new_shape = (ny, ky, nx, kx) + X.shape[2:]
    return np.nanmean(X_pad.reshape(new_shape), axis=(1, 3))


class Heatmap:
    def __init__(self, width, height, color=("white", "bright_black")):
        self.height = height
        self.width = width
        self.data = None
        self.color = color

    def update(self, data):
        assert len(data.shape) <= 2
        if len(data.shape) == 1:
            self.data = np.expand_dims(data, axis=0)
        else:
            self.data = data

    def show(self):
        full_x = self.data.shape[1]
        full_y = self.data.shape[0]
        kx = full_x // self.width // 2
        ky = full_y // self.height // 4
        if kx <= 0 or ky <= 0:
            d = self.data
        else:
            d = pool(self.data, (ky, kx))
        c = plotille.Canvas(
            self.width, self.height, xmax=d.shape[1] + 1, ymax=d.shape[0] + 1
        )
        mean = np.mean(d)
        if self.color:
            std = np.std(d) / 2
            for x in range(d.shape[0]):
                for y in range(d.shape[1]):
                    if d[x, y] > mean + std:
                        c.point(x, y, color=self.color[0])
                    elif d[x, y] < mean - std:
                        c.point(x, y, color=self.color[1])
                    else:
                        c.point(x, y, set_=False)
        else:
            for x in range(d.shape[0]):
                for y in range(d.shape[1]):
                    if d[x, y] > mean:
                        c.point(x, y)
                    else:
                        c.point(x, y, set_=False)
        c.rect(0, 0, d.shape[1], d.shape[0])
        return c.plot()

    def __str__(self):
        return self.show()


def horiz_center(a, b, center):
    la = len(a)
    lb = len(b)
    to_pad = None
    if la > lb:
        to_pad = b
        pad = la - lb
    elif lb > la:
        to_pad = a
        pad = lb - la
    else:
        return a, b
    pre = pad // 2
    post = pad - pre
    if not center:
        post = pre + post
        pre = 0
    to_pad[:0] = ["" for i in range(pre)]
    to_pad[len(to_pad) :] = ["" for i in range(post)]
    return a, b


def horiz_concat(*args, padding=1, center=True):
    assert len(args) >= 2
    out = args[0]
    for arg in args[1:]:
        out = horiz_concat_impl(out, arg, padding, center)
    return out


ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")


def horiz_concat_impl(s0, s1, padding, center):
    s0 = str(s0).replace("\t", "  ")
    s1 = str(s1).replace("\t", "  ")
    l0 = s0.split("\n")
    l1 = s1.split("\n")
    l0, l1 = horiz_center(l0, l1, center)
    assert len(l0) == len(l1)
    l0 = [l.rstrip() for l in l0]
    noansi_l0 = [ansi_escape.sub("", l) for l in l0]
    max_len = max([len(l) for l in noansi_l0]) + padding
    new_l0 = []
    for l, noansi_l in zip(l0, noansi_l0):
        new_l0.append(l + " " * (max_len - len(noansi_l)))
    l0 = new_l0
    ls = [a + b for a, b in zip(l0, l1)]
    return "\n".join(ls)


class TextBuffer:
    def __init__(self, width, height, accumulate=True):
        self.width = width
        self.height = height
        self.accumulate = accumulate
        self.data = []

    def update(self, *args):
        data = " ".join(str(a) for a in args)
        if self.accumulate:
            self.data += data.split("\n")
            self.data = self.data[-self.height :]
        else:
            self.data = data.split("\n")

    def show(self):
        d = self.data[-self.height :]
        return "\n".join(l[: self.width] for l in d)

    def __str__(self):
        return self.show()


class Reprint:
    def __init__(self, auto_flush=False):
        self.h = 0
        self.s = ""
        self._print = builtins.print
        self.auto_flush = auto_flush
        self.callers = set()

    def add(self, s):
        self.s += ("\n" if self.s else "") + s

    def print(self, *args, **kwargs):
        if self.auto_flush:
            caller = getframeinfo(stack()[1][0])
            n = caller.filename + ":" + str(caller.lineno)
            if n in self.callers:
                self.flush()
            self.callers.add(n)
        self.add(" ".join([str(arg) for arg in args]))

    def flush(self):
        esc = chr(27)
        back = esc + "[1F"
        clr_line = esc + "[0K"
        self._print(back * self.h, end="")
        lines = self.s.split("\n")
        self.h = len(lines)
        for l in lines:
            self._print(f"{l}{clr_line}")
        self.s = ""
        self.callers = set()

    def __enter__(self):
        print(chr(27) + "[?25l", end="")
        builtins.print = self.print
        return self

    def __exit__(self, type, value, traceback):
        if self.auto_flush:
            self.flush()
        builtins.print = self._print
        print(chr(27) + "[?25h", end="")
