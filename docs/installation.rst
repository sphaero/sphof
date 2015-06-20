Installation
------------

.. :note:
   You're machine should come preinstalled with the Sphof module.

Operating System installation
#############################
You should install the latest Python version on your machine

For the Pillow module you'll need to make sure you have the Tcl/Tk
libraries and includes installed

.. code-block:: bash

   $ sudo apt-get install tcl-dev tcl tk tk-dev python3-tk


Required Python modules
#######################

The :py:mod:`sphof` module requires the following modules:

* Pillow
* Pyre
* pyZOCP

You can install these using 'pip':

.. code-block:: bash

   $ pip install Pillow
   $ pip install pyzmq
   $ pip install https://github.com/zeromq/pyre/archive/master.zip
   $ pip install https://github.com/z25/pyZOCP/archive/master.zip

.. note::
   On some operating systems 'pip' is named 'pip3' or 'pip-3.2'
