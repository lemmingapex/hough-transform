#!/usr/bin/python -O
# -*- coding: utf-8 -*-

import string, sys
import os.path
import argparse
import numpy
import math
import scipy.misc
import cv2
from cv2 import imread, imwrite

class HoughTransform:
	def __init__(self):
		return

	def execute(self, image, angle_resolution):
		thetas = numpy.deg2rad(numpy.arange(-90.0, 90.0, angle_resolution))
		y_length, x_length = image.shape
		max_distance = int(math.ceil(math.sqrt(y_length*y_length + x_length*x_length)))
		number_of_thetas = len(thetas)
		hough_space = numpy.zeros((2*max_distance, number_of_thetas));
		max_bin_size = 0;

		cos_thetas = numpy.cos(thetas)
		sin_thetas = numpy.sin(thetas)

		for y in range(y_length):
			for x in range(x_length):
				if image[y][x] == 255:
					for i_theta in range(number_of_thetas):
						pho = int(math.ceil(x*cos_thetas[i_theta] + y*sin_thetas[i_theta]))
						hough_space[max_distance + pho][i_theta] += 1
						if(hough_space[max_distance + pho][i_theta] > max_bin_size):
							max_bin_size = hough_space[max_distance + pho][i_theta]

		# normalize the output space to 0 to 255:
		for y in range(hough_space.shape[0]):
			for x in range(hough_space.shape[1]):
				hough_space[y][x]*=(255.0/max_bin_size)

		# resize the image
		hough_space = scipy.misc.imresize(hough_space, size=image.shape)

		return hough_space

# main (DRIVER)
def main():
	parser = argparse.ArgumentParser(description="Hough Transform")
	parser.add_argument("input_filename", help="jpg or png input image file path")
	parser.add_argument("-a", "--angle_resolution", type=float, default=1.0, metavar="angle_resolution", help="Angle resolution in degrees.  180/angle_resolution number of bins.  A lower angle value may give you more acurate lines, but will take longer to run.  The angle_resolution you choose must divide 180 without remainder: 180%angle_resolution == 0.")
	args = parser.parse_args()

	input_filename = args.input_filename
	if not os.path.isfile(input_filename):
		print "ERROR: The file \""+ input_filename + "\" does not exist.\n"
		return 1
	if not input_filename.endswith(".jpg") and not input_filename.endswith(".png"):
		print "ERROR: This is not an .jpg or .png file.\n"
		return 2
	outputFileName = "output.png"

	image = imread(input_filename, cv2.IMREAD_GRAYSCALE).astype("int32")
	angle_resolution = args.angle_resolution

	houghImage = HoughTransform().execute(image, angle_resolution)
	imwrite(outputFileName, houghImage)
	return 0

# call to main
if __name__ == "__main__":
	main()
