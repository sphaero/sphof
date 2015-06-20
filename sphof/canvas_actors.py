#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import logging
from random import randint
from PIL import Image, ImageDraw, ImageTk
import sphof
from .actors import Actor, LeadActor

logger = logging.getLogger(__name__)

try:
    import tkinter
except:
    logger.warn("No Tkinter installed")
    pass


class Painter(object):
    """
    The Painter class provides simple methods for drawing, ie:
    
    * :py:meth:`.line`
    * :py:meth:`.rectangle`
    * :py:meth:`.ellipse`
    * :py:meth:`.arc`

    The default width and height are 200 by 600 pixels.
    
    Each class's method is documented below
    """
    def __init__(self, *args, **kwargs):
        self._img = None
        self._d = None
        self.background_color = (15,15,15)
        self.width = 200
        self.height = 600
        self.reset()
        super(Painter, self).__init__(*args, **kwargs)

    def reset(self):
        """
        Clears the image to the background color
        """
        self._img = Image.new("RGB", (self.width,self.height), self.background_color)
        self._d = ImageDraw.Draw(self._img)

    def get_width(self):
        """
        Returns the width of the canvas
        """
        return self.width

    def set_width(self, width):
        """
        Set the width of the canvas
        :param width: Width of the canvas in pixels
        """
        self.width = width

    def get_height(self):
        """
        Returns the height of the canvas
        """
        return 600

    def set_height(self, height):
        """
        Set the height of the canvas
        :param width: Width of the canvas in pixels
        """
        self.height = height

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


class PainterActor(Painter, Actor):
    """
    The PainterActor class is an :py:class:`sphof.Actor` with all the 
    :py:class:`sphof.Painter` class's methods and providing methods to handover
    the image to a LeadActor.

    example:

    .. code-block:: python

        from sphof import PainterActor
        
        class MyPainter(PainterActor):

            def setup():
                self.count = 0                   # initialize counter

            def update():
                self.count += 1                  # increment counter
                if self.count == 60:
                    self.count = 0               # reset counter
                    self.send_img()              # emit the imgID so a 
                                                 # LeadActor could 
                                                 # display it

            def draw():
                start = (self.count, self.count) # start position
                end = (50, 100 - self.count)     # end position
                color = (
                        randint(70,110),         # red
                        randint(160,210),        # green
                        randint(70,210)          # blue
                        )
                self.line(start, end, color, 2)  # draw line

    To display the PainterActor's drawing you need to send the image
    to CanvasActor which can display the image on screen. In order to
    send an image use the :py:meth:`.send_img` method.
    
    The :py:meth:`.send_img` method emits a imgID signal containing a 
    pointer to the image of this Actor. It class reset() so the actor
    can paint a new image. 

    This class has many methods inherited from the 
    :py:class:`sphof.Painter` class, ie:

    * :py:meth:`.line`
    * :py:meth:`.rectangle`
    * :py:meth:`.ellipse`
    * :py:meth:`.arc`

    Each class's extra methods are documented below.
    """

    def __init__(self, *args, **kwargs):
        self._count = 0  #fps counter
        # run the actor
        super(PainterActor, self).__init__(*args, **kwargs)
        self.register_int("imgID", id(self._img), 're')

    def send_img(self):
        """
        Sends the image as a signal to any subscribers
        """
        imgID = id(self._img)
        sphof.shared_ns[imgID] = self._img
        self.emit_signal("imgID", imgID)


class CanvasActor(Painter, LeadActor):
    """
    The CanvasActor class implements methods for drawing on a canvas (screen)

    .. code-block:: python

        from sphof import CanvasActor
        
        class MyPainter(CanvasActor):

            def setup(self):
                self.count = 0                   # initialize counter

            def update():
                self.count += 1                  # increment counter
                self.count = self.count % 50     # counter bound

            def draw():
                start = (self.count, self.count) # start position
                end = (50, 100 - self.count)     # end position
                color = (
                        randint(70,110),         # red
                        randint(160,210),        # green
                        randint(70,210)          # blue
                        )
                self.line(start, end, color, 2)  # draw line

    To display drawings of PainterActor you need to receive the image
    of the PainterActor by subscribing to a signal emitted by the
    PainterActor.

    .. code-block:: python

        from sphof import CanvasActor
        
        class MyPainter(CanvasActor):

            def setup(self):
                self.register_int("PaintingID", 0, "re") # create a sensor of image ids

            def on_enter_peer(self, peer, name, data):
                if name == "PainterName":       # PainterName is the name of the PainterActor
                    self.signal_subscribe(self.uuid(), "PaintingID", peer, "PaintingID")

            def on_peer_signaled(self, peer, name, data):
                if name == "PainterName":
                    self.draw_painting(data.value)

            def draw():
                start = (self.count, self.count) # start position
                end = (50, 100 - self.count)     # end position
                color = (
                        randint(70,110),         # red
                        randint(160,210),        # green
                        randint(70,210)          # blue
                        )
                self.line(start, end, color, 2)  # draw line


    """
    def __init__(self, *args, **kwargs):
        self._display = tkinter.Tk()
        self.canvas = tkinter.Canvas(self._display, width=800, height=600)
        self.canvas.pack()
        self._display.bind("<Button>", self._button_click_exit_mainloop)

        super(CanvasActor, self).__init__(*args, **kwargs)
        self._image = ImageTk.PhotoImage(self._img)
        self.canvas.create_image(0, 0, image=self._image, anchor='nw')

    def _button_click_exit_mainloop(self, event):
        event.widget.quit() # this will cause mainloop to unblock.

    def draw_img(self, img, x, y):
        """
        Draw the image at position x,y
        """
        self.canvas.create_image(x, y, image=img, anchor='nw')

    def post_draw(self):
        """
        Display the painting on the TK canvas
        """
        self._display.update()


if __name__ == '__main__':
    test1 = ZCanvas_t("Thread1")
    test2 = ZCanvas_t("Thread2")
    try:
        test1.thread.join()
        test2.thread.join()
    except Exception as e:
        print(e)
    finally:
        test1.stop()
        test2.stop()
        print("FINISHED")
