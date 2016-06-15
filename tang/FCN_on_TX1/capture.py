# -*- coding=utf-8 -*-
import time
import numpy as np
import subprocess as sp
import signal
import sys
import os.path
import glob

class Capture:
    def __init__(self, imgdir='/tmp', width=1280, height=720):
        self.imgdir = imgdir
        self.width = width
        self.height = height

        assert (width, height) == (1280, 720), '還沒實作其他解析度的命令.....'

        cmd = 'nvgstcapture-1.0 -m 1 --image-res=3 --file-name=%s/my' % imgdir # 3:1280*720
        self.p = sp.Popen(cmd, shell=True, stdin=sp.PIPE)
        self.stdin = self.p.stdin
        time.sleep(1)
        
    def __del__(self):
        self.stdin.write('q\n')
        print 'terminating..'

    def capture(self):
        # cmd = 'gst-launch-1.0 -e nvcamerasrc fpsRange="30.0 30.0" ! \'video/x-raw(memory:NVMM), width=(int)1920, height=(int)1080, format=(string)I420, framerate=(fraction)30/1\' ! nvvidconv flip-method=2 ! \'video/x-raw(memory:NVMM), format=(string)I420\'  !  nvjpegenc ! filesink location=%s -e'
        
        self.stdin.write('j\n')
        time.sleep(0.1)
        
        newest = max(glob.iglob(self.imgdir + '/my*.jpg'), key=os.path.getctime)
        return newest


if __name__ == '__main__':
    cap = Capture()
    for i in xrange(5):
        print cap.capture()
        time.sleep(1)
