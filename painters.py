import tkinter
import time
import logging
import ctypes
from random import randint
from PIL import Image, ImageDraw, ImageTk
from zocp import ZOCP
from sys import getrefcount as grc

from sphof.canvas_actors import CanvasActor
from mypainter import MyPainter

logger = logging.getLogger(__name__)

class Painters(ZOCP):

    def __init__(self, *args, **kwargs):
        super(Painters, self).__init__(*args, **kwargs)

        self._display = tkinter.Tk()
        self.canvas = tkinter.Canvas(self._display, width=800, height=600)
        self.canvas.pack()
        self._display.bind("<Button>", self._button_click_exit_mainloop)

        self.setup()
        self.start()
        self._loop()

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
        self._painters = [
            MyPainter("Thread1"),
            MyPainter("Thread2"),
            MyPainter("Thread3"),
            MyPainter("Thread4")
        ]

    def on_peer_enter(self, peer, name, *args, **kwargs):
        print("ENTER", peer, name)
        if name == "Thread1":
            self.signal_subscribe(peer, "rmId", self.uuid(), "id1")
            self.signal_subscribe(self.uuid(), "Painter1", peer, "imgId")
        if name == "Thread2":
            self.signal_subscribe(peer, "rmId", self.uuid(), "id2")
            self.signal_subscribe(self.uuid(), "Painter2", peer, "imgId")
        if name == "Thread3":
            self.signal_subscribe(peer, "rmId", self.uuid(), "id3")
            self.signal_subscribe(self.uuid(), "Painter3", peer, "imgId")
        if name == "Thread4":
            self.signal_subscribe(peer, "rmId", self.uuid(), "id4")
            self.signal_subscribe(self.uuid(), "Painter4", peer, "imgId")

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
            # this is a really nasty hack to prevent copying the image
            # http://stackoverflow.com/questions/1396668/python-get-object-by-id
            imgID = data[1]
            img = ctypes.cast(imgID, ctypes.py_object).value
            #self._orig_images[0] = img
            self._images[0] = ImageTk.PhotoImage(img)
            self.emit_signal("id1", imgID)
        elif name == "Thread2":
            imgID = data[1]
            img = ctypes.cast(imgID, ctypes.py_object).value
            #self._orig_images[1] = img
            self._images[1] = ImageTk.PhotoImage(img)
            self.emit_signal("id2", imgID)
        elif name == "Thread3":
            imgID = data[1]
            img = ctypes.cast(imgID, ctypes.py_object).value
            #self._orig_images[2] = img
            self._images[2] = ImageTk.PhotoImage(img)
            self.emit_signal("id3", imgID)
        elif name == "Thread4":
            imgID = data[1]
            img = ctypes.cast(imgID, ctypes.py_object).value
            #self._orig_images[3] = img
            self._images[3] = ImageTk.PhotoImage(img)
            self.emit_signal("id4", imgID)

    def update(self):
        for i, img in enumerate(self._images):
            if img:
                self.canvas.create_image(i*200, 0, image=img, anchor='nw')
        #self._display.update()
        
    def draw(self):
        self._display.update()

    def _button_click_exit_mainloop (event):
        event.widget.quit() # this will cause mainloop to unblock.

    def _loop(self):
        self._running = True
        t = time.time()
        try:
            reap_at = time.time() + 10/10.
            while self._running:
                timeout = reap_at - time.time()
                if timeout < 0:
                    timeout = 0
                self.run_once(timeout * 1000)
                reap_at = time.time() + 10/10.
                
                self.update()
                self.draw()

        except Exception as e:
            print(e)
        finally:
            self._running = True
            for t in self._painters:
                t.stop()
            self.stop()


if __name__ == '__main__':
    test = Painters("Painter")
