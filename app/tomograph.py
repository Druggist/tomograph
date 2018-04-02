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
        self.detector_count = detector_count if detector_count % 2 == 1 else detector_count + 1
        self.detector_width = detector_width
        self.orginal_img = np.array(Image.open(image_path).convert('L'))
        self.radius = min(self.orginal_img.shape) / 2
        if self.detector_count * self.detector_width > self.radius * 2:
            sys.exit("Too many detectors or detectors are too wide.")
        self.step = 0
        self.sinogram = np.zeros((int(180 / self.alpha), self.detector_count))
        self.constructed_img = np.ones(self.orginal_img.shape)
        self.detectors = None
        self.mask = self._generate_mask()

    def get_error(self):
        res = np.add(-np.min(self.constructed_img), self.constructed_img)
        res = np.divide(res, np.max(res))
        res = np.multiply(res, 255)
        return np.sqrt(np.mean(np.abs(self.orginal_img - res)**2))

    def _generate_mask(self):
        mask = []
        for i in range(int(-self.detector_count / 2), int(self.detector_count / 2) + 1):
            if i == 0:
                mask.append(1)
            elif i % 2 == 0:
                mask.append(0)
            else:
                mask.append((-4 / (np.pi ** 2)) / (i ** 2))
        return mask

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

    def measure(self, with_mask=False):
        detectors = self._get_detectors()
        for i, d in enumerate(detectors):
            line = d.get_connecting_line_points()
            summ = 0
            for p in line:
                summ += self.orginal_img[p[0]][p[1]]
            average = summ / len(line)
            self.sinogram[self.step][i] = int(average)
        if with_mask:
            self.sinogram[self.step] = np.convolve(self.sinogram[self.step], self.mask)[int(self.detector_count / 2): -int(self.detector_count / 2)]

    def construct(self):
        detectors = self._get_detectors()
        for i, d in enumerate(detectors):
            line = d.get_connecting_line_points()
            for p in line:
                self.constructed_img[p[0]][p[1]] += self.sinogram[self.step][i]

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
