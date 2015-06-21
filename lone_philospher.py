#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
from sphof import LonePhilosopherActor

class SinglePhilospher(LonePhilosopherActor):

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
                print("Jay food! Eating....", len(self.topics))
            else:
                print("Hmmmmm... let me think...", len(self.topics))
            
        if not self.state_hungry:
            enlightenment = self.think()
            if enlightenment:
                print("".join(["#"]*70))
                print("{0}: Eureka... {1}".format(self.name(), enlightenment))
                print("".join(["#"]*70))
        else:
            self.eat()


if __name__ == '__main__':
    test = SinglePhilospher("Descartes")
    test.run()
