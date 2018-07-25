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

	def write_lines(self, image, hough_space, angle_resolution):
		# find the bins brighter than threshold_percent*255 for the addtion of lines
		threshold_percent = 0.7
		threshold = int(threshold_percent*255)

		y_length, x_length = image.shape
		thetas = numpy.deg2rad(numpy.arange(-90.0, 90.0, angle_resolution))
		max_distance = int(math.ceil(math.sqrt(y_length*y_length + x_length*x_length)))
		for i_pho in range(hough_space.shape[0]):
			for i_theta in range(hough_space.shape[1]):
				if hough_space[i_pho][i_theta] >= threshold:
					theta = thetas[i_theta]
					pho = i_pho - max_distance
					a = math.cos(theta)
					b = math.sin(theta)
					x0 = a*pho
					y0 = b*pho
					x1 = int(x0 + 10000*(-b))
					y1 = int(y0 + 10000*(a))
					x2 = int(x0 - 10000*(-b))
					y2 = int(y0 - 10000*(a))
					cv2.line(image,(x1,y1),(x2,y2),120)
		return image

	def get_normalized_hough_space(self, image, angle_resolution):
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
		for pho in range(hough_space.shape[0]):
			for theta in range(hough_space.shape[1]):
				hough_space[pho][theta]*=(255.0/max_bin_size)

		return hough_space


	def execute(self, image, angle_resolution, write_hough_space):
		hough_space = self.get_normalized_hough_space(image, angle_resolution)
		output_image = None;
		if write_hough_space:
			# resize the space to match the image
			output_image = scipy.misc.imresize(hough_space, size=image.shape)
		else:
			output_image = self.write_lines(image, hough_space, angle_resolution)

		return output_image

# main (DRIVER)
def main():
	parser = argparse.ArgumentParser(description="Hough Transform")
	parser.add_argument("input_filename", help="jpg or png input image file path")
	parser.add_argument("-a", "--angle_resolution", type=float, default=1.0, metavar="angle_resolution", help="Angle resolution in degrees.  180/angle_resolution number of bins.  A lower angle value may give you more acurate lines, but will take longer to run.  The angle_resolution you choose must divide 180 without remainder: 180%angle_resolution == 0.")
	parser.add_argument("-w", "--write_hough_space", action="store_true", help="Outputs an image of the hough space instead of the orginal image with lines.")
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
	write_hough_space = args.write_hough_space

	outputImage = HoughTransform().execute(image, angle_resolution, write_hough_space)
	imwrite(outputFileName, outputImage)
	return 0

# call to main
if __name__ == "__main__":
	main()
