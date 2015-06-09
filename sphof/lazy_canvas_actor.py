#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import logging
import tkinter
import threading
from random import randint
from PIL import Image, ImageDraw, ImageTk
from zocp import ZOCP
from sys import getrefcount as grc
import ctypes
logger = logging.getLogger(__name__)

"""
.. module:: canvas_actors
   :platform: Unix, Windows
   :synopsis: A module for drawing on a canvas using ZOCP.

.. moduleauthor:: Arnaud Loonstra <arnaud@sphaero.org>
"""

class LazyCanvasActor(ZOCP):

    """The LazyCanvasActors class provides simple methods for drawing on a canvas

    Just inherit from this class and implement a setup, update and draw method, i.e.:

    .. code-block:: python

        from sphof import LazyCanvasActor
        
        class MyPainter(LazyCanvasActor):

            def setup():
                self.count = 0

            def update():
                self.count += 1
                self.count = self.count % 50

            def draw():
                start = self.count
                end = 100 - self.count
                self.line(start, end, 2)

    This class has many method for drawing on a canvas, ie:

    * :py:meth:`.LazyCanvasActor.line`
    * :py:meth:`.arc`

    Each class's method is documented below.
    """


    def __init__(self, *args, **kwargs):
        super(LazyCanvasActor, self).__init__(*args, **kwargs)
        if kwargs.get("imagefile"):
            self._img = Image.open(kwargs.get("imagefile"))
        else:
            self._img = Image.new("RGB", (200,600), (255,255,55))
        self._d = ImageDraw.Draw(self._img)

        self._display = tkinter.Tk()
        self.canvas = tkinter.Canvas(self._display, width=200, height=600)
        self.canvas.pack()
        #self.canvas.image = ImageTk.PhotoImage(self._img)
        #self.canvas.create_image(0, 0, image=self.canvas.image, anchor='nw')
        self._display.bind("<Button>", self._button_click_exit_mainloop)
        #self.canvas.image = ImageTk.PhotoImage(self._img)
 
        self.start()
        self.setup()
        self._loop()

    def setup(self):
        """
        Called a startup.
        
        Add variables here
        i.e.::

            self.count = 0

        and in update()::

            count += 1

        """
        logger.warning("Please implement a setup method!!!")

    def update(self):
        """
        Called every loop
        """
        logger.warning("Please implement an update method!!!")

    def draw(self):
        """
        Called after update to draw the canvas on screen
        """
        self.canvas.image1 = ImageTk.PhotoImage(self._img)
        self.canvas.create_image(0, 0, image=self.canvas.image1, anchor='nw')
        self._display.update()

    def reset(self):
        """
        Clears the image to the background color
        """
        self._img = Image.new("RGB", (200,600), self.background_color)
        self._d = ImageDraw.Draw(self._img)

    def get_width(self):
        """
        Returns the width of the canvas
        """
        return 200

    def get_height(self):
        """
        Returns the height of the canvas
        """
        return 600


    def arc(self, *args, **kwargs):
        """
        Draws an arc (a portion of a circle outline) between the start and end
        angles, inside the given bounding box.

        :param xy: Four points to define the bounding box. Sequence of
            ``[(x0, y0), (x1, y1)]`` or ``[x0, y0, x1, y1]``.
        :param start: Starting angle, in degrees. Angles are measured from
                3 o'clock, increasing clockwise.
        :param end: Ending angle, in degrees.
        :param fill: Color to use for the arc.
        """
        self._d.arc(*args, **kwargs)

    def bitmap(self, *args, **kwargs):
        """        
        Draws a bitmap (mask) at the given position, using the current fill color
        for the non-zero portions. The bitmap should be a valid transparency mask
        (mode “1”) or matte (mode “L” or “RGBA”).

        This is equivalent to doing ``image.paste(xy, color, bitmap)``.

        To paste pixel data into an image, use the
        :py:meth:`~PIL.Image.Image.paste` method on the image itself.
        """
        self._d.bitmap(*args, **kwargs)

    def chord(self, *args, **kwargs):
        """
        Same as :py:meth:`~PIL.ImageDraw.Draw.arc`, but connects the end points
        with a straight line.

        :param xy: Four points to define the bounding box. Sequence of
                ``[(x0, y0), (x1, y1)]`` or ``[x0, y0, x1, y1]``.
        :param outline: Color to use for the outline.
        :param fill: Color to use for the fill.
        """
        self._d.chord(*args, **kwargs)

    def ellipse(self, *args, **kwargs):
        """
        Draws an ellipse inside the given bounding box.

        :param xy: Four points to define the bounding box. Sequence of either
                ``[(x0, y0), (x1, y1)]`` or ``[x0, y0, x1, y1]``.
        :param outline: Color to use for the outline.
        :param fill: Color to use for the fill.
        """
        self._d.ellipse(*args, **kwargs)

    def line(self, *args, **kwargs):
        """
        Draws a line between the coordinates in the **xy** list.

        :param xy: Sequence of either 2-tuples like ``[(x, y), (x, y), ...]`` or
                   numeric values like ``[x, y, x, y, ...]``.
        :param fill: Color to use for the line.
        :param width: The line width, in pixels. Note that line
               joins are not handled well, so wide polylines will not look good.        
        """
        self._d.line(*args, **kwargs)

    def pieslice(self, *args, **kwargs):
        """
        Same as arc, but also draws straight lines between the end points and the
        center of the bounding box.

        :param xy: Four points to define the bounding box. Sequence of
                ``[(x0, y0), (x1, y1)]`` or ``[x0, y0, x1, y1]``.
        :param start: Starting angle, in degrees. Angles are measured from
                3 o'clock, increasing clockwise.
        :param end: Ending angle, in degrees.
        :param fill: Color to use for the fill.
        :param outline: Color to use for the outline.        
        """
        self._d.pieslice(*args, **kwargs)

    def point(self, *args, **kwargs):
        """
        Draws points (individual pixels) at the given coordinates.

        :param xy: Sequence of either 2-tuples like ``[(x, y), (x, y), ...]`` or
                   numeric values like ``[x, y, x, y, ...]``.
        :param fill: Color to use for the point.        
        """
        self._d.point(*args, **kwargs)

    def polygon(self, *args, **kwargs):
        """ 
        Draws a polygon.

        The polygon outline consists of straight lines between the given
        coordinates, plus a straight line between the last and the first
        coordinate.

        :param xy: Sequence of either 2-tuples like ``[(x, y), (x, y), ...]`` or
                   numeric values like ``[x, y, x, y, ...]``.
        :param outline: Color to use for the outline.
        :param fill: Color to use for the fill.       
        """
        self._d.polygon(*args, **kwargs)

    def rectangle(self, *args, **kwargs):
        """
         Draws a rectangle.

        :param xy: Four points to define the bounding box. Sequence of either
                ``[(x0, y0), (x1, y1)]`` or ``[x0, y0, x1, y1]``. The second point
                is just outside the drawn rectangle.
        :param outline: Color to use for the outline.
        :param fill: Color to use for the fill.       
        """
        self._d.rectangle(self, *args, **kwargs)

    def text(self, *args, **kwargs):
        """
        Draws the string at the given position.

        :param xy: Top left corner of the text.
        :param text: Text to be drawn.
        :param font: An :py:class:`~PIL.ImageFont.ImageFont` instance.
        :param fill: Color to use for the text.        
        """
        self._d.text(*args, **kwargs)
    
    def textsize(self, *args, **kwargs):
        """
        Return the size of the given string, in pixels.

        :param text: Text to be measured.
        :param font: An :py:class:`~PIL.ImageFont.ImageFont` instance.        
        """
        self._d.textsize(*args, **kwargs)

    def _button_click_exit_mainloop (event):
        event.widget.quit() # this will cause mainloop to unblock.

    def _loop(self):
        self._running = True
        count = 0
        t = time.time()
        try:
            reap_at = time.time() + 1/60.
            while self._running:
                timeout = reap_at - time.time()
                if timeout < 0:
                    timeout = 0
                self.run_once(0) #timeout * 1000)
                reap_at = time.time() + 1/60.

                self.update()
                self.draw()
                count += 1
                if t + 60 < time.time():
                    print("{0}: fps: {1}".format(self.name, count/((time.time() - t))))
                    t = time.time()
                    count = 0
        except Exception as e:
            print(e)
        finally:
            self.stop()


if __name__ == '__main__':
    # Normal Actor
    test = LazyCanvasActor("TEST")
