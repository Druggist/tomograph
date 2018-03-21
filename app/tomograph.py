#!/usr/bin/python

import numpy as np
import sys
from PIL import Image


class Detector:
    def __init__(self, a, b, x, y):
        self.a = int(a)
        self.b = int(b)
        self.x = int(x)
        self.y = int(y)
        self.line = self._get_connecting_line_points()

    def get_connecting_line_points(self):
        return self.line

    def _get_connecting_line_points(self):
        line = []
        dx = self.x - self.a
        dy = self.y - self.b

        xsign = 1 if dx > 0 else -1
        ysign = 1 if dy > 0 else -1

        dx = abs(dx)
        dy = abs(dy)

        if dx > dy:
            xx, xy, yx, yy = xsign, 0, 0, ysign
        else:
            dx, dy = dy, dx
            xx, xy, yx, yy = 0, ysign, xsign, 0

        D = 2 * dy - dx
        y = 0

        for x in range(dx + 1):
            line.append((self.a + x * xx + y * yx - 1, self.b + x * xy + y * yy - 1))
            if D >= 0:
                y += 1
                D -= 2 * dx
            D += 2 * dy
        return line


class Tomograph:
    def __init__(self, alpha, detector_count, detector_width, image_path):
        self.alpha = alpha
        self.current_alpha = 0
        self.detector_count = detector_count
        self.detector_width = detector_width
        self.orginal_img = np.array(Image.open(image_path).convert('L'))
        self.radius = min(self.orginal_img.shape) / 2
        if self.detector_count * self.detector_width > self.radius * 2:
            sys.exit("Too many detectors or detectors are too wide.")
        self.step = 0
        self.sinogram = np.zeros((self.detector_count, int(180 / self.alpha)))
        self.constructed_img = np.ones(self.orginal_img.shape)
        self.detectors = None

    def _get_detectors(self):
        if self.detectors is not None:
            return self.detectors
        self.detectors = [
            Detector(
                self.radius - self.radius * np.cos(np.deg2rad(self.current_alpha + self.detector_width * i)),
                self.radius + self.radius * np.sin(np.deg2rad(self.current_alpha + self.detector_width * i)),
                self.radius - self.radius * np.cos(np.deg2rad(self.current_alpha + 180 % 360 + self.detector_width * ((self.detector_count - 1) - i))),
                self.radius + self.radius * np.sin(np.deg2rad(self.current_alpha + 180 % 360 + self.detector_width * ((self.detector_count - 1) - i)))
            ) for i in range(self.detector_count)
        ]
        return self.detectors

    def measure(self):
        detectors = self._get_detectors()
        for i, d in enumerate(detectors):
            line = d.get_connecting_line_points()
            summ = 0
            for p in line:
                summ += self.orginal_img[p[0]][p[1]]
            average = summ / len(line)
            self.sinogram[i][self.step] = int(average)

    def construct(self):
        detectors = self._get_detectors()
        for i, d in enumerate(detectors):
            line = d.get_connecting_line_points()
            for p in line:
                self.constructed_img[p[0]][p[1]] += self.sinogram[i][self.step]**3

    def normalize(self):
        max_val = self.constructed_img.max()
        min_val = self.constructed_img.min()

        for i in range(len(self.constructed_img)):
            for j in range(len(self.constructed_img[i])):
                self.constructed_img[i][j] = self.constructed_img[i][j] - min_val / (max_val - min_val)

    def next_step(self):
        self.detectors = None
        self.step += 1
        self.current_alpha = self.current_alpha + self.alpha

# tmp = Tomograph(90, 1, 2, "./data/test_color.png")
# tmp.getDetectorPoints()gi
# tmp.nextStep()
# tmp.getDetectorPoints()
