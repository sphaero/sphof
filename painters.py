#!/usr/bin/python 
# -*- coding: utf-8 -*-
import tkinter
import time
import logging
import ctypes
from random import randint
from PIL import Image, ImageDraw, ImageTk
from zocp import ZOCP
from sys import getrefcount as grc

import sphof
from sphof import CanvasActor
from mypainter import MyPainter

logger = logging.getLogger(__name__)

class Painters(CanvasActor):

    def setup(self):
        self.register_int("Painter1", 0, "rs")
        self.register_int("Painter2", 0, "rs")
        self.register_int("Painter3", 0, "rs")
        self.register_int("Painter4", 0, "rs")
        self.register_int("id1", 0, "re")
        self.register_int("id2", 0, "re")
        self.register_int("id3", 0, "re")
        self.register_int("id4", 0, "re")
        self._count = 0
        self.painter_images = [None,None,None,None]
        self.add_actor(MyPainter("Thread1"))
        self.add_actor(MyPainter("Thread2"))
        self.add_actor(MyPainter("Thread3"))
        self.add_actor(MyPainter("Thread4"))

    def on_peer_enter(self, peer, name, *args, **kwargs):
        print("ENTER", peer, name)
        if name == "Thread1":
            self.signal_subscribe(self.uuid(), "Painter1", peer, "imgID")
        if name == "Thread2":
            self.signal_subscribe(self.uuid(), "Painter2", peer, "imgID")
        if name == "Thread3":
            self.signal_subscribe(self.uuid(), "Painter3", peer, "imgID")
        if name == "Thread4":
            self.signal_subscribe(self.uuid(), "Painter4", peer, "imgID")

    def on_peer_exit(self, peer, name, *args, **kwargs):
        print("EXIT", peer, name)
        if name == "Thread1":
            self.painter_images[0] = None
        if name == "Thread2":
            self.painter_images[1] = None
        if name == "Thread3":
            self.painter_images[2] = None
        if name == "Thread4":
            self.painter_images[3] = None
    
    def on_peer_signaled(self, peer, name, data, *args, **kwargs):
        #logger.warning("ZOCP PEER SIGNALED: %s modified %s" %(name, data))
        if name == "Thread1":
            imgID = data[1]
            self.painter_images[0] = self.get_img_from_id(imgID)
        elif name == "Thread2":
            imgID = data[1]
            self.painter_images[1] = self.get_img_from_id(imgID)
        elif name == "Thread3":
            imgID = data[1]
            self.painter_images[2] = self.get_img_from_id(imgID)
        elif name == "Thread4":
            imgID = data[1]
            self.painter_images[3] = self.get_img_from_id(imgID)

    def draw(self):
        for i, img in enumerate(self.painter_images):
            if img:
                self.draw_img(img, i*200, 0)


if __name__ == '__main__':
    logger = logging.getLogger("zocp")
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())
    logger.propagate = False
    test = Painters("Painter")
    print("run app")
    test.run()
