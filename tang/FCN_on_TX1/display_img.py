# -*- coding=utf-8 -*-
import cv2
import os.path
import glob

def display():
	while True:
		# newest image path
		img_path = max(glob.iglob('/home/ubuntu/fcn.berkeleyvision.org/out/combined*.jpg'), key=os.path.getctime)
		img = cv2.imread(img_path)
		cv2.imshow('image', img)
		cv2.waitKey(500)
		print "next frame"

if __name__ == '__main__':
	display()
