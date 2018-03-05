#!/usr/bin/python

import numpy as np
from PIL import Image

class Tomograph:
	def __init__(self, alpha, detectorCount, detectorWidth, imagePath):
		self.alpha
		self.detectorCount = detectorCount
		self.detectorWidth = detectorWidth
		self.orginalImg=np.array(Image.open(imagePath).convert('L'))

	def getAlpha(self):
		return self.alpha

	def getDetectorCount(self):
		return self.detectorCount

	def getDetectorWidth(self):
		return self.detectorWidth
