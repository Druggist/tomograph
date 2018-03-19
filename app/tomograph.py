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

    def get_connecting_line_points(self):
        x = self.a
        y = self.b
        if self.a < self.x:
            xi = 1
            dx = self.x - self.a
        else:
            xi = -1
            dx = self.a - self.x
        if self.b < self.y:
            yi = 1
            dy = self.y - self.b
        else:
            yi = -1
            dy = self.b - self.y
        line = [(x, y)]
        if dx > dy:
            ai = (dy - dx) * 2
            bi = dy * 2
            d = bi - dx
            while x != self.x:
                if d >= 0:
                    x += xi
                    y += yi
                    d += ai
                else:
                    d += bi
                    x += xi
                line.append((x, y))
        else:
            ai = (dx - dy) * 2
            bi = dx * 2
            d = bi - dy
            while y != self.y:
                if d >= 0:
                    x += xi
                    y += yi
                    d += ai
                else:
                    d += bi
                    y += yi
                line.append((x, y))
        return line


class Tomograph:
    def __init__(self, alpha, detector_count, detector_width, image_path):
        self.alpha = alpha
        self.current_alpha = 0
        self.detector_count = detector_count if detector_count % 2 == 1 else detector_count + 1
        self.detector_width = detector_width
        self.orginal_img = np.array(Image.open(image_path).convert('L'))
        self.radius = min(len(self.orginal_img), len(self.orginal_img[0])) / 2
        if self.detector_count * self.detector_width >= self.radius * 2:
            sys.exit("Too many detectors or detectors are too wide.")
        self.step = 0
        self.sinogram = []
        self.constructed_img = np.array([[0 for col in range(len(self.orginal_img[0]))] for row in range(len(self.orginal_img))])

    def _get_detectors(self):
        tmp = []
        for i in range(self.detector_count):
            start = (self.radius - self.radius * np.cos(np.deg2rad(self.current_alpha + self.detector_width * i)),
                     self.radius + self.radius * np.sin(np.deg2rad(self.current_alpha + self.detector_width * i)))
            end = (self.radius - self.radius * np.cos(
                np.deg2rad(self.current_alpha + 180 % 360 + self.detector_width * i)),
                   self.radius + self.radius * np.sin(
                       np.deg2rad(self.current_alpha + 180 % 360 + self.detector_width * i)))
            tmp.append((start, end))

        # parallel lines between detectors do not cross in center of image
        detectors = []
        for i in range(len(tmp)):
            detectors.append(Detector(tmp[-1 - i][0][0], tmp[-1 - i][0][1], tmp[i][1][0], tmp[i][1][1]))
        return detectors

    def measure(self):
        detectors = self._get_detectors()
        row = []
        for d in detectors:
            line = d.get_connecting_line_points()
            summ = 0
            for p in line:
                summ += self.orginal_img[p[0]-1][p[1]-1]
            average = summ/len(line)
            row.append(int(average))
        self.sinogram.append(row)
        return row

    def construct(self, step):
        detectors = self._get_detectors()
        it = 0
        for d in detectors:
            line = d.get_connecting_line_points()
            for p in line:
                self.constructed_img[p[0]-1][p[1]-1] = self.sinogram[step][it]
            it += 1

    def normalize(self):
        max_val = self.constructed_img.max()
        min_val = self.constructed_img.min()

        for i in range(len(self.constructed_img)):
            for j in range(len(self.constructed_img[i])):
                self.constructed_img[i][j] = self.constructed_img[i][j] - min_val / (max_val - min_val)


    def next_step(self):
        self.step += 1
        self.current_alpha = self.current_alpha + self.alpha if self.current_alpha + self.alpha < 360 else 0

# tmp = Tomograph(90, 1, 2, "./data/test_color.png")
# tmp.getDetectorPoints()
# tmp.nextStep()
# tmp.getDetectorPoints()
