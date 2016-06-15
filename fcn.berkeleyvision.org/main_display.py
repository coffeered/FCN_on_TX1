import numpy as np
from PIL import Image
import caffe
import score
import time
import matplotlib.pyplot as plt

# load image, switch to BGR, subtract mean, and make dims C x H x W for Caffe
im = Image.open('data/pascal/VOC2010/JPEGImages/2007_000129_500x500.jpg')
in_ = np.array(im, dtype=np.float32)
in_ = in_[:,:,::-1]
in_ -= np.array((104.00698793,116.66876762,122.67891434))
in_ = in_.transpose((2,0,1))

# load net
#net = caffe.Net('voc-fcn8s/deploy.prototxt', 'voc-fcn8s/fcn8s-heavy-pascal.caffemodel', caffe.TEST)
net = caffe.Net('voc-fcn-alexnet/deploy.prototxt', 'voc-fcn-alexnet/train_iter_16000.caffemodel', caffe.TEST)

# shape for input (data blob is N x C x H x W), set data
net.blobs['data'].reshape(1, *in_.shape)
net.blobs['data'].data[...] = in_
# run net and take argmax for prediction

# add
"""
net.params['score_fr'][0].data[...]=np.load('score_fr0')
net.params['score_fr'][1].data[...]=np.load('score_fr1')
ggg=np.load('upscore')
net.params['upscore'][0].data[...]=np.resize(ggg,(63,63))
"""
# add end

net.forward()
time.sleep(30);
out = net.blobs['score'].data[0].argmax(axis=0)
#print out


#display
#fig = plt.imshow(net.blobs['score'].data[0][15], cmap="jet") 
fig = plt.imshow(net.blobs['score'].data[0][15], cmap="seismic") 
plt.axis('off') 
fig.axes.get_xaxis().set_visible(False) 
fig.axes.get_yaxis().set_visible(False) 
plt.savefig('test_output.jpg', bbox_inches='tight', pad_inches=0)

