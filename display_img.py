import cv2

def display(img_path):
	while True:
		img = cv2.imread(img_path)
		cv2.imshow('image', img)
		cv2.waitKey(1000)
		print "next frame"

display("./logo.png")
