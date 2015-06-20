Guide
-----

In this test we will create programs which enable the use of multiple
processors of a computer. You will be provided with a framework and some
tools to create a program for the assignment.

This website provides the description of the assignments as well as a
reference for the framework and tools.

Introduction
############

In the framework we call a small program an 'Actor'. The :py:mod:`sphof`
framework provides different 'Actor' classes. These classes have a 
setup(), update() and draw() method similar to OpenFrameworks.

Additionally to these methods there are methods to enable communication
between the Actors. Communication is done using signals which you'll need
to use during the assignments.

Using the Actor classes you can register variables to be used for 
communication between actors. I.e.:

.. code-block:: python

   class MyFirstActor(Actor):

       def setup(self):
           self.register_int("MyFirstInt", 0, "rs")
            
       def update():
           self.emit_signal("MyFirstInt", self.get_value("MyFirstInt")+1)

It's important to understand that once an Actor has a variable 
registered every other Actor can access this value. However before
reading the value of a variable the Actor interested in the variable
first needs to subscribe to it. This can be accomplished by using the 
signal_subscribe method. I.e:

.. code-block:: python

    class MySecondActor(Actor):

        def on_enter_peer(self, peer_id, peer_name, *args, **kwargs):
            self.signal_subscribe(self.uuid(),  None, peer, "MyFirstInt")

        def on_peer_signaled(self, peer_id, name, signal):
            print(name, signal)

By subscribing to the variable of an Actor the Actor will send the value
to you. Of course you first need to be aware of the Actor you are 
interested in hence the usage of the 'on_enter_peer' method. Remember 
as we are running Actors on multiple processors you will never know if 
your program started first or if the other was first. Therefore the 
'on_enter_peer' method will tell you.

It might also be easier to directly link the variable of an Actor to
your own variable. You can do this by registering your variable and then
subscribing your variable to the other Actor's variable. The code for
'MySecondActor' then becomes:

.. code-block:: python

    class MySecondActor(Actor):

        def setup(self):
            self.register_int("MySecondInt", 0, "rs")

        def on_enter_peer(self, peer_id, peer_name, *args, **kwargs):
            self.signal_subscribe(self.uuid(),  "MySecondInt", peer, "MyFirstInt")

        def update(self):
            print(self.get_value('MyOtherInt')

Test 1: Painters Spree
######################

In the first test you will need to display the drawings of multiple
painters. You need to use the :doc:`Canvas Actor classes <canvas_actors>`
for these have simple methods for drawing.

