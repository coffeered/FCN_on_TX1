import os.path
import glob
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def display():
	img_dir = '/home/ubuntu/fcn.berkeleyvision.org/capture/'
	heat_dir = '/home/ubuntu/fcn.berkeleyvision.org/out/'

	print 'start'

	fig = plt.figure()

	img_path = max(glob.iglob(img_dir + 'my*.jpg'), key=os.path.getctime)
	heat_path = max(glob.iglob(heat_dir + '*.jpg'), key=os.path.getctime)

	print img_path
	print heat_path

	img = mpimg.imread(img_path)
	heat_img = mpimg.imread(heat_path)

	imgplot = plt.imshow(img)
	plt.hold(True)
	imgplot = plt.imshow(heat_img, alpha=.5)

	plt.savefig('out_img.jpg')

	print 'done'

if __name__ == '__main__':
	display()
