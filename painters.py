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
        self._orig_images = [None,None,None,None]
        self._images = [None,None,None,None]
        self.actors.extend([
            MyPainter("Thread1"),
            MyPainter("Thread2"),
            MyPainter("Thread3"),
            MyPainter("Thread4")
        ])

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
            self._orig_images[0] = None
            self._images[0] = None
        if name == "Thread2":
            self._orig_images[1] = None
            self._images[1] = None
        if name == "Thread3":
            self._orig_images[2] = None
            self._images[2] = None
        if name == "Thread4":
            self._orig_images[3] = None
            self._images[3] = None
    
    def on_peer_signaled(self, peer, name, data, *args, **kwargs):
        #logger.warning("ZOCP PEER SIGNALED: %s modified %s" %(name, data))
        if name == "Thread1":
            imgID = data[1]
            img = sphof.shared_ns.pop(imgID)
            self._images[0] = ImageTk.PhotoImage(img)
        elif name == "Thread2":
            imgID = data[1]
            img = sphof.shared_ns.pop(imgID)
            self._images[1] = ImageTk.PhotoImage(img)
        elif name == "Thread3":
            imgID = data[1]
            img = sphof.shared_ns.pop(imgID)
            self._images[2] = ImageTk.PhotoImage(img)
        elif name == "Thread4":
            imgID = data[1]
            img = sphof.shared_ns.pop(imgID)
            self._images[3] = ImageTk.PhotoImage(img)

    def update(self):
        start = (randint(0,200), randint(0,600))
        end = (randint(0,200), randint(0,600))
        color = (randint(70,110), 0, 0)
        self.line([start, end], color, 10)
        
    def draw(self):
        for i, img in enumerate(self._images):
            if img:
                self.draw_img(img, i*200, 0)
        self._display.update()


if __name__ == '__main__':
    logger = logging.getLogger("zocp")
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    logger.propagate = False
    test = Painters("Painter")
