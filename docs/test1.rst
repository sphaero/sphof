Test 1: Painters Spree
----------------------

*Imagine you have created a simple application that draws something on the
screen. Your processor is not fast enough to draw 60 frames per second.*

In this first test we will create a program which handles multiple
painters. This is often a problem in concurrent programs as OpenGL and 
most graphic libraries can only run in the main thread. Therefore it is
impossible to let multiple Actors draw on the display. We will need to
workaround this limitation.

You need to use the :doc:`Canvas Actor classes <canvas_actors>`
for these have simple methods for drawing. First start by creating
a simple painter using the :py:class:`sphof.LoneActor` class:

.. code-block:: python

   from sphof import LonePainterActor
   from random import randint

   class SinglePainter(LonePainterActor):

       def setup(self):
           self.set_width(800)
           self.set_height(600)

       def draw(self):
           start = (
               randint(0, self.get_width()),   # x coordinate
               randint(0, self.get_height())   # y coordinate
               )
           end = (
               randint(0, self.get_width()),   # x coordinate
               randint(0, self.get_height())   # y coordinate
               )
           color = (
               randint(70,110),                # red color
               randint(160,210),               # green color
               randint(70,210)                 # blue color
               )
           self.line([start, end], color, 20)

   painter = SinglePainter("SinglePainter")
   painter.run()

This runs on a single processor. Now if we would want to have multiple 
painters using multiple processors we need to create an Actor for 
displaying and other Actors for creating the drawings. As you read in 
the :doc:`guide <guide>` you can use a :py:class:`LeadActor` to start 
other Actors. You can now understand that this :py:class:`LeadActor` 
also needs to display the drawings as it will be the only Actor 
with access to the display of the computer!

PainterActor and CanvasActor Class
##################################

The :py:class:`PainterActor <sphof.PainterActor>` class provides a 
:py:meth:`send_img <sphof.PainterActor.send_img>` method for 
signalling a new image. The :py:class:`PainterActor <sphof.PainterActor>` 
class also automatically registers the 'imgID' variable which is a 
reference to the image. Therefore you can simply call :py:meth:`send_img <sphof.PainterActor.send_img>`
to send the image. However there is one rule of thumb: Once you send the 
image you do not own it anymore!

The :py:class:`CanvasActor <sphof.PainterActor>` class provides a 
:py:meth:`get_img_from_id <sphof.CanvasActor.draw_img_from_id>` method.
You can pass the imgID value and it will return the image. You can then
use :py:meth:`draw_img <sphof.CanvasActor.draw_img>` to display the image.

*Why these methods? You have to understand that you cannot just pass images
around like that. An image occupies a large amount of memory and copying
them takes a large amount of time. Therefore the sending happens by passing a
reference instead of the full image. In languages like C or C++ you'd
call this a pointer. This is a bit difficult in a language like Python
because if we would send the image it will be garbage collected after
being send. Anyway, these are just convenience methods to prevent you from 
running into trouble and keeping your machine performant.*
