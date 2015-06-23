Test 1: Painters Spree
----------------------

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
               randint(0, self.get_height())     # y coordinate
               )
           end = (
               randint(0, self.get_width()),   # x coordinate
               randint(0, self.get_height())     # y coordinate
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
also needs to display as it will be the only one with access to the 
display!

.. note::
    The :py:class:`PainterActor <sphof.PainterActor>` class provides a 'send_img' method for 
    signalling a new image. The :py:class:`PainterActor <sphof.PainterActor>` 
    class also automatically registers the 'imgID' variable which is a 
    reference to the image. The :py:class:`CanvasActor <sphof.CanvasActor>` 
    is a LeadActor! It has the method 'draw_img' which accepts the imgID value.
