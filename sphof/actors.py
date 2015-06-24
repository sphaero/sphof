#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import logging
import threading
from zocp import ZOCP

logger = logging.getLogger(__name__)

"""
Package Example (:mod:`actors`)
==================================

.. currentmodule:: actors
.. autosummary::
   :toctree:

   LoneActor
   Actor
   LeadActor
"""

class LoneActor(object):
    """
    The LoneActor class runs an application loop.
    
    :param str name: Name of the node, if not given a random name will be created
    
    By default the LoneActor loop runs at 60 iterations per second. This 
    means your update and draw method is called every 1/60th second.
    
    * Use the :py:meth:`.LoneActor.setup` method to setup the class
    * Use :py:meth:`.LoneActor.update` method to update anything you\
    have setup
    * Use :py:meth:`.LoneActor.draw` method to visualise
    """    
    def __init__(self, name, *args, **kwargs):
        self._name = name
        super(LoneActor, self).__init__(*args, **kwargs)
        self.setup()
        
    def setup(self):
        """
        Called a startup.
        
        Add variables you want to use througout the actor here.
        I.e.::

            self.count = 0

        and in the update() method::

            self.count += 1

        """
        logger.warning("{0}:No setup method implemented!!!".format(self.name()))
    
    def pre_update(self):
        return

    def update(self):
        """
        Called every loop
        """
        logger.warning("{0}:No update method implemented!!!".format(self.name()))
        self.update = self._dummy

    def post_update(self):
        return

    def pre_draw(self):
        return

    def draw(self):
        """
        Called after update
        """
        return
        logger.warning("{0}:No draw method implemented!!!".format(self.name()))
        self.draw = self._dummy

    def post_draw(self):
        return

    def name(self):
        return self._name

    def run(self):
        self._running = True
        count = 0
        t = time.time()
        try:
            reap_at = time.time() + 1/60.
            while self._running:
                timeout = reap_at - time.time()
                if timeout > 0:
                    #timeout = 0
                    time.sleep(timeout)
                else:
                    logger.debug("Can't do 60 fps")
                #self.run_once(0) #timeout * 1000)
                reap_at = time.time() + 1/60.

                self.pre_update()
                self.update()
                self.post_update()

                self.pre_draw()
                self.draw()
                self.post_draw()
                
                count += 1
                if t + 60 < time.time():
                    print("{0}: fps: {1}".format(self.name(), (time.time() - t)/count))
                    t = time.time()
                    count = 0
        except (KeyboardInterrupt, SystemExit) as e:
            print(e)

    def _dummy(self, *args, **kwargs):
        pass


class Actor(ZOCP):
    """
    An Actor class runs inside its own thread. It's usually started
    by a LeadActor!
    
    :param str name: Name of the node, if not given a random name will be created

    By default the Actor loop runs at 60 iterations per second. This 
    means your update and draw method is called every 1/60th second.
    
    * Use the :py:meth:`.Actor.setup` method to setup the class
    * Use the :py:meth:`.Actor.update` method to update anything you\
    have setup
    * Use the :py:meth:`.Actor.draw` method to visualize
    
    .. warning::
        It is important to understand that an actor runs in a thread.
        Usually a thread is started by a 'main' thread. A :py:class:`sphof.LeadActor` 
        provides methods for starting and stopping Actors as the 
        LeadActor runs in the main thread. An Actor has limitations. For 
        example you cannot visualize directly from an Actor. To 
        visualize what an actor draws you'll need to handover the image 
        to a LeadActor.
    """
    def __init__(self, *args, **kwargs):
        super(Actor, self).__init__(*args, **kwargs)
        self.setup()
        self.start()
    
    def setup(self):
        """
        Called a startup.
        
        Add variables you want to use througout the actor here.
        I.e.::

            self.count = 0

        and in the update() method::

            self.count += 1

        """
        logger.warning("{0}:No setup method implemented!!!".format(self.name()))

    def start(self):
        ZOCP.start(self)                            # Start ZOCP        
        self.thread = threading.Thread(target=self.run)
        self.thread.daemon = True
        self.thread.start()                         # And run loop
        print(self.name(), "started")

    def pre_update(self):
        return
    
    def update(self):
        """
        Called every loop
        """
        logger.warning("{0}:No update method implemented!!!".format(self.name()))
        self.update = self._dummy

    def post_update(self):
        return

    def pre_draw(self):
        return
        
    def draw(self):
        """
        Called after update
        """
        return
        logger.warning("{0}:No draw method implemented!!!".format(self.name()))
        self.draw = self._dummy
    
    def post_draw(self):
        return
        
    def run(self):
        """
        Run the actor's application loop
        """
        self._running = True
        t = time.time()
        count = 1
        try:
            reap_at = time.time() + 1/60.
            while self._running:
                timeout = reap_at - time.time()
                if timeout < 0:
                    timeout = 0
                # set next interval
                reap_at = time.time() + 1/60.
                self.run_once(timeout * 1000)   # parse ZOCP queue

                self.pre_update()
                self.update()
                self.post_update()

                self.pre_draw()
                self.draw()
                self.post_draw()
 
                count += 1
                # stats
                if t + 60 < time.time():
                    print("{0}: fps: {1}".format(self.name(), count/(time.time() - t)))
                    t = time.time()
                    count = 1

        except (KeyboardInterrupt, SystemExit) as e:
            logger.warning("Actor {0} finished. Exception:{1}".format(self.name(), e))
        finally:
            self._running = False
            self.stop()
        logger.warning("Actor {0} finished.".format(self.name()))
    
    def _dummy(self, *args, **kwargs):
        pass


class LeadActor(Actor):
    """
    A LeadActor class runs in the main thread. It inherits all methods 
    from the Actor class but has some additional methods to start Actors 
    
    :param str name: Name of the node, if not given a random name will be created
        
    By default the LeadActor loop runs at 60 iterations per second. This 
    means your update and draw method is called every 1/60th second.
    
    * Use the :py:meth:`.Actor.setup` method to setup the class
    * Use :py:meth:`.Actor.update` method to update anything you\
    have setup
    * Use :py:meth:`.Actor.draw` method to visualise
    """
    
    def __init__(self, *args, **kwargs):
        self.actors = set()
        super(LeadActor, self).__init__(*args, **kwargs)
    
    def start(self):
        ZOCP.start(self)

    def stop(self):
        """
        Stop this LeadActor. Before stopping all Actors started
        from this LeadActor are stopped first
        """
        for act in self.actors:
            act.stop()
        # call our original stop method
        Actor.stop(self)

    def add_actor(self, actor):
        """
        Add an Actor and run its threaded loop
        
        :param Actor actor: An Actor to start in its own thread
        
        .. warning:
            You cannot add a LeadActor as only one LeadActor can run
            in the main thread!
        """
        self.actors.add(actor)
        
    def remove_actor(self, actor):
        """
        Remove and stop an Actor
        
        :param Actor actor: An Actor to remove and stop
        """
        try:
            self.actors.remove(actor)
        except KeyError:
            log.warning("Actor unknown: ".format(actor))
        else:
            actor.stop()
