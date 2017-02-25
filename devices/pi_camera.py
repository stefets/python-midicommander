#!/usr/bin/env python
#-*- coding: utf-8 -*-

import picamera

class Camera(object):
    def __init__(self):

        print "Initializing camera..."
        self.camera = picamera.PiCamera()
        #self.effects = dict({0:"none", 1:"sketch", 2:"negative", 3:"colorswap" })
        self.effects = dict({0:"none", 1:"negative", 2:"solarize", 3:"sketch", 4:"denoise", 
            5:"emboss", 6:"oilpaint", 7:"hatch", 8:"gpen", 9:"pastel", 10:"watercolor", 11:"film", 
            12:"blur", 13:"saturation", 14:"colorswap",15:"washedout", 16:"posterise", 17:"colorpoint", 
            18:"colorbalance", 19:"cartoon", 20:"deinterlace1", 21:"deinterlace2" })
        self.rotation = dict({0:0, 1:90, 2:180, 3:270, 99:-1 })
        self.camera.image_effect = 'none'
        self.camera.zoom = (0.0,0.0,1.0,1.0)
        self.index = -1

    def start_preview(self):
        self.camera.image_effect = 'none'
        self.camera.zoom = (0.0,0.0,1.0,1.0)
        self.camera.start_preview() 

    def stop_preview(self):
        self.camera.stop_preview()

    def zoom_width(self, value):
        h = self.camera.zoom[3]
        w = float(value)/100
        self.camera.zoom = (0.0,0.0,w,h)

    def zoom_height(self, value):
        w = self.camera.zoom[2]
        h = float(value)/100
        self.camera.zoom = (0.0,0.0,w,h)

    def zoom_x(self, value):
        z = self.camera.zoom
        x = float(value)/100
        zoom = (x,z[1],x,z[3])
        #print zoom
        self.camera.zoom = zoom

    def zoom_y(self, value):
        z = self.camera.zoom
        x = float(value)/100
        zoom = (z[0],x,z[2],x)
        #print zoom
        self.camera.zoom = zoom
        
    def flip(self):
        self.camera.vflip = bool(random.getrandbits(1))
        self.camera.hflip = bool(random.getrandbits(1))

    def capture(self):
        filename = str(uuid.uuid4()) + '.jpg'
        self.camera.capture(filename)

    def set_rotation(self, index):
        if index != 99:
            self.camera.rotation = self.rotation[index]
        else:
            if self.camera.rotation == 270:
                self.camera.rotation = 0
            else:
                self.camera.rotation += 90

    def set_effect(self, index):
        self.camera.image_effect = 'none'
        if index >= 0 and index <= 21:
            self.camera.image_effect = self.effects[index]
        else:
            self.index += 1
            if self.index > 21:
                self.index = 0
            self.camera.image_effect = self.effects[self.index]

    def execute(self, data1, data2):
        if data1 == 20:
            if data2 == 1:
                self.start_preview()
            elif data2 == 2:
                self.stop_preview()
            else:
                pass
        elif data1 == 21:
            self.set_effect(data2)
        elif data1 == 22:
            self.set_rotation(data2)
        elif data1 == 23:
            self.capture()
        elif data1 == 25:
            self.zoom_width(data2)
        elif data1 == 26:
            self.zoom_height(data2)
        elif data1 == 27:
            self.zoom_x(data2)
        elif data1 == 28:
            self.zoom_y(data2)
        elif data1 == 29:
            self.flip()
        else:
            pass
        
    def dispose(self):
        self.camera.stop_preview()
        self.camera.close()
        del self.camera
