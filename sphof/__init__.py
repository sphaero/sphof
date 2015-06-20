#!/usr/bin/python 
# -*- coding: utf-8 -*-
#__all__ = ['canvas_actors']
#__all__ = ['pyre', 'zbeacon', 'zhelper']

from .actors import LoneActor, LeadActor, Actor
from .canvas_actors import CanvasActor, PainterActor, Painter

shared_ns = {}      # this is the shared namespace used for passing pointers
                    # id(var) : var
                    # this works for multiple threads because of the GIL
                    # otherwise use one ns per thread
#__license__ = "Cecill-C"
#__revision__ = " $Id: actor.py 1586 2009-01-30 15:56:25Z cokelaer $ "
#__docformat__ = 'reStructuredText'
