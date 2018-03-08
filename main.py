#!/usr/bin/python

import numpy as np
import sys
from PIL import Image

class Tomograph:
	def __init__(self, alpha, detectorCount, detectorWidth, imagePath):
		self.alpha = alpha
		self.currentAlpha = 0
		self.detectorCount = detectorCount if detectorCount % 2 == 1 else detectorCount + 1
		self.detectorWidth = detectorWidth
		self.orginalImg = np.array(Image.open(imagePath).convert('L'))
		self.radius = min(len(self.orginalImg), len(self.orginalImg[0])) / 2
		if self.detectorCount * self.detectorWidth >= self.radius * 2:
			sys.exit("Too many detectors or detectors are too wide.")

	def getAlpha(self):
		return self.alpha

	def getDetectorCount(self):
		return self.detectorCount

	def getDetectorWidth(self):
		return self.detectorWidth

	def getDetectorPoints(self):
		detectors = []
		for detector in range(self.detectorCount):
			#TODO Shift detectors
			start = (self.radius + self.radius * np.cos(np.deg2rad(self.currentAlpha)), self.radius + self.radius * np.sin(np.deg2rad(self.currentAlpha)))
			end =  (self.radius + self.radius * np.cos(np.deg2rad(self.currentAlpha + 180 % 360)), self.radius + self.radius * np.sin(np.deg2rad(self.currentAlpha + 180 % 360)))
			detectors.append((start, end))
		print(detectors)	

	def nextStep(self):
		self.currentAlpha = self.currentAlpha + self.alpha if self.currentAlpha + self.alpha < 360 else 0


tmp = Tomograph(90,1,2,"./data/test_color.png")
tmp.getDetectorPoints() 
tmp.nextStep() 
tmp.getDetectorPoints() 