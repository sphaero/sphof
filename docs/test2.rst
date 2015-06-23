Test 2: Dining Philosophers
---------------------------

In the second test we will search for a solution of a typical computer
science problem. Five philosophers sit at a round table with bowls of
rice. Chopsticks are placed between each pair of adjacent philosophers.  

.. image:: philtable.png

Each philosopher must alternately think and eat. However, a philosopher 
can only eat rice when he has both left and right chopstick. Each 
chopstick can be held by only one philosopher and so a philosopher can 
use the chopstick only if it is not being used by another philosopher. 
After he finishes eating, he needs to put down both chopsticks so 
they become available to others. A philosopher can take the chopstick on
his right or the one on his left as they become available, but cannot 
start eating before getting both of them.

There is an infinite amount of rice in the bowls.

You need to design a program which makes sure all philosophers can think
and eat. There are many solutions to this problem but you are adviced to
use a waiter which serves the table. 

In the framework a :py:class:`PhilosopherActor<sphof.PhilosopherActor>` 
class is provided. This actor has the methods :py:meth:`think<sphof.PhilosopherActor.think>`
and :py:meth:`eat<sphof.PhilosopherActor.eat>`. If a  philosopher is in the 
thinking state the :py:meth:`think<sphof.PhilosopherActor.think>` method 
needs to be called. If the philosopher is in the eating  state the 
:py:meth:`eat<sphof.PhilosopherActor.eat>` method needs to be called. 
A single philosopher implementation is given below:

.. code-block:: python

    import time
    from sphof import LonePhilosopherActor

    class SinglePhilosopher(LonePhilosopherActor):

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
                    print("Eureka:", enlightenment, len(self.topics))
            else:
                self.eat()


    if __name__ == '__main__':
        test = SinglePhilosopher("Descartes")
        test.run()

You can use this implementation for your multiple philosophers 
implementation. 
