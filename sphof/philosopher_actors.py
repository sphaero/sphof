#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import logging
import random
import sphof
from sphof import Actor, LeadActor, LoneActor

logger = logging.getLogger(__name__)

class Philosopher(object):
    """
    The Philospher class provides the think and eat method.
    """
    def __init__(self, *args, **kwargs):
        self.topics = []                      # food for thought
        super(Philosopher, self).__init__(*args, **kwargs)        

    def think(self):
        """
        The think methods makes the philospher actor think about 
        something and determine the quality of it. If the quality
        is good it will return the thought. Otherwise it returns None
        
        If the philospher is out of topics it will say so. He then needs
        to eat.
        """
        topic = self._get_text()            # get a text
        if topic:
            rnd = random.random()           # estimate quality
            if rnd > 0.99:                  # if it is good
                return topic                # return the thought
            else:
                return None                 # else return nothing
        else:
            print("{0}:Out of topics, need food for thought".format(self.name()))

    def eat(self):
        """ 
        The eat method makes the philosopher eat. This fills its list
        of topics for thinking (food for thought)
        """
        self.topics.append("Blablabla{0}".format(len(self.topics)))
        #time.sleep(0.1)                 # crunch

    def _get_text(self):
        try:
            return self.topics.pop()
        except IndexError:
            return None

class PhilosopherActor(Philosopher, Actor):
    
    def __init__(self, *args, **kwargs):
        super(PhilosopherActor, self).__init__(*args, **kwargs)
    
class LonePhilosopherActor(Philosopher, LoneActor):
    
    def __init__(self, *args, **kwargs):
        super(LonePhilosopherActor, self).__init__(*args, **kwargs)

