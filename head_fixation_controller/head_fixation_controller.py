import json
from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Net import *
from Phidget22.Devices.Stepper import *
from Phidget22.Devices.DigitalInput import *
from Phidget22.Devices.VoltageRatioInput import *

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

    _PHIDGETS_CONFIGURATION_FILENAME = "phidgets.json"

    def __init__(self,*args,**kwargs):
        if 'debug' in kwargs:
            self.debug = kwargs['debug']

        with open(self._PHIDGETS_CONFIGURATION_FILENAME) as f:
            phidgets_configuration_json = f.read()

        self._phidgets_configuration = json.loads(phidgets_configuration_json)

        self._phidgets = {}
        for name, phidget_configuration in self._phidgets_configuration.items():
            try:
                if (phidget_configuration["channel_class"] == "Stepper"):
                    self._phidgets.update({name : Stepper()})
                elif (phidget_configuration["channel_class"] == "DigitalInput"):
                    self._phidgets.update({name : DigitalInput()})
                elif (phidget_configuration["channel_class"] == "VoltageRatioInput"):
                    self._phidgets.update({name : VoltageRatioInput()})
                else:
                    break
                self._phidgets[name].name = name
                self._phidgets[name].setDeviceSerialNumber(phidget_configuration["device_serial_number"])
                self._phidgets[name].setHubPort(phidget_configuration["hub_port"])
                self._phidgets[name].setChannel(phidget_configuration["channel"])
                self._phidgets[name].setOnAttachHandler(self._phidget_attached)
                self._phidgets[name].open()
            except KeyError:
                break

        for name, phidget in self._phidgets.items():
            print(name, phidget.name, phidget.getAttached())

    def _phidget_attached(self,attached):
        print(attached.getChannelName())

# -----------------------------------------------------------------------------------------
if __name__ == '__main__':

    debug = False
    dev = HeadFixationController(debug=debug)
