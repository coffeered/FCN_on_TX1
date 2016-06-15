import numpy as np
from PIL import Image
import caffe
import score
import time
import matplotlib.pyplot as plt
from capture import Capture
import itertools,math
import cv2

import matplotlib.image as mpimg

W = 256
H = 144

def main():

    cap = Capture('./capture')

    # load net
    #net = caffe.Net('voc-fcn8s/deploy.prototxt', 'voc-fcn8s/fcn8s-heavy-pascal.caffemodel', caffe.TEST)
    net = caffe.Net('voc-fcn-alexnet/deploy.prototxt', 'voc-fcn-alexnet/train_iter_16000.caffemodel', caffe.TEST)

    for i in xrange(500):
        imgfile = cap.capture()
        run(net, imgfile, 'out/', '%d.jpg' % i)

def run(net, imgfile, outdir, outfile):
    print 'Running:', imgfile

    # load image, switch to BGR, subtract mean, and make dims C x H x W for Caffe
    im = Image.open(imgfile).resize((W, H))
    in_ = np.array(im, dtype=np.float32)
    in_ = in_[:,:,::-1]
    in_ -= np.array((104.00698793,116.66876762,122.67891434))
    in_ = in_.transpose((2,0,1))

    # shape for input (data blob is N x C x H x W), set data
    net.blobs['data'].reshape(1, *in_.shape)
    net.blobs['data'].data[...] = in_
    # run net and take argmax for prediction

    print 'forward start'
    net.forward()
    out = net.blobs['score'].data[0].argmax(axis=0)
    print 'forward done'

    human = 15
    heatmap = net.blobs['score'].data[0][human]

    # mask(im, heatmap)
    # im.save(outdir + outfile + 'g.png')

    #display
    fig = plt.imshow(heatmap, cmap="seismic")
    plt.axis('off')
    fig.axes.get_xaxis().set_visible(False)
    fig.axes.get_yaxis().set_visible(False)
    plt.savefig(outdir + outfile, bbox_inches='tight', pad_inches=0)

    fig_show = plt.figure()
    plt.axis('off')
    img = mpimg.imread(imgfile)
    imgplot = plt.imshow(img)
    plt.hold(True)
    heat_img = mpimg.imread(outdir + outfile)
    heat_img = cv2.resize(heat_img, (1280, 720))
    # heat_img = heat_img.imresize(heat_img, [1280, 720])
    imgplot = plt.imshow(heat_img, alpha=.5)
    # plt.show()
    plt.savefig(outdir + 'combined' + outfile)
    plt.close(fig_show)

    print 'Output:', outdir + outfile

def mask(im, heatmap):
    ## heatmap: H x W
    data = np.array(im) # H x W
    # print 'data shape', data.shape
    heatmap=np.fabs(heatmap);
    h_max=np.max(heatmap)
    h_min=np.min(heatmap)
    pixels = im.load() # W x H
    #threshold=np.median(heatmdap)
    for x,y in itertools.product(range(W), range(H)):
        heatmap[y,x]=heatmap[y,x]-h_min/h_max-h_min
        if(heatmap[y,x]<0.3):
            heatmap[y,x]=0.3
        pixels[x,y]=tuple(data[y,x]*heatmap[y,x])
        """
        if heatmap[y,x]>threshold:
            pixels[x,y] = tuple(data[y, x])
        else:
            dd=data[y,x]*0.1
            pixels[x,y]= tuple(dd.astype(int))
        """
if __name__ == '__main__':
    main()
