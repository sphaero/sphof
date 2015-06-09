#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import logging
import random
import tkinter
from PIL import Image, ImageDraw, ImageTk
from zocp import ZOCP

logger = logging.getLogger(__name__)

class LonePhilospher(object):

    def __init__(self, *args, **kwargs):
        self.setup()
        self._run()

    def setup(self):
        self.state_hungry = True
        self.switch_at = time.time() + 5      # switch state every 5s
        self.enlightenment = None
        self.topics = []                      # food for thought

    def update(self):
        if time.time() > self.switch_at or not(len(self.topics)):
            # it's time to switch state
            self.switch_at = time.time() + 5    # set next state switch timestamp
            self.state_hungry = not(self.state_hungry)
            if self.state_hungry:
                print("I'm hungry, eating....", len(self.topics))
            else:
                print("Hmmmmm... let me think...", len(self.topics))
            
        if not self.state_hungry:
            enlightenment = self.think()
            if enlightenment:
                print("Eureka:", enlightenment, len(self.topics))
        else:
            self.eat()

    def think(self):
        topic = self._get_text()            # get a text
        if topic:
            rnd = random.random()           # estimate quality
            if rnd > 0.9999:                # if it is good
                return topic                # return the thought
            else:
                return None                 # else return nothing
        else:
            print("Out of topics, need food for thought")
            
    def eat(self):
        self.topics.append("Blablabla{0}".format(len(self.topics)))
        #time.sleep(0.1)                 # crunch
    
    def stop(self):
        pass
        
    def _get_text(self):
        try:
            return self.topics.pop()
        except IndexError:
            return None
    
    def _run(self):
        self._running = True
        count = 0
        t = time.time()
        try:
            reap_at = time.time() + 1/600.       # 60fps
            while self._running:
                timeout = reap_at - time.time()
                if timeout < 0:
                    timeout = 0
                time.sleep(timeout)
                #self.run_once(timeout * 1000)
                reap_at = time.time() + 1/600.        

                self.update()
                #self.draw()
                #count += 1
                #if t + 60 < time.time():
                #    print("{0}: fps: {1}".format(self.name, count/((time.time() - t))))
                #    t = time.time()
                #    count = 0
        except KeyboardInterrupt as e:
            print(e)
        finally:
            self.stop()


if __name__ == '__main__':
    # Normal Actor
    test = LonePhilospher("TEST")
