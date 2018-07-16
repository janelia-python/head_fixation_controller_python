from __future__ import print_function, division
import time
import atexit
import os
from datetime import datetime
from threading import Timer
import csv

from modular_client import ModularClients

try:
    from pkg_resources import get_distribution, DistributionNotFound
    _dist = get_distribution('head_fixation_controller')
    # Normalize case for Windows systems
    dist_loc = os.path.normcase(_dist.location)
    here = os.path.normcase(__file__)
    if not here.startswith(os.path.join(dist_loc, 'head_fixation_controller')):
        # not installed, but there is another version that *is*
        raise DistributionNotFound
except (ImportError,DistributionNotFound):
    __version__ = None
else:
    __version__ = _dist.version


DEBUG = False

class HeadFixationController():
    '''
    HeadFixationController.

    Example Usage:

    dev = HeadFixationController() # Might automatically find devices if available
    '''

    def __init__(self,*args,**kwargs):
        if 'debug' in kwargs:
            self.debug = kwargs['debug']


# -----------------------------------------------------------------------------------------
if __name__ == '__main__':

    debug = False
    dev = HeadFixationController(debug=debug)
