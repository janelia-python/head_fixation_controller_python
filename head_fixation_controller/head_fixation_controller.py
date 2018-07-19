import json
from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Net import *
from Phidget22.Devices.Stepper import *
from Phidget22.Devices.DigitalInput import *
from Phidget22.Devices.VoltageRatioInput import *
import os

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

class LatchController():
    '''
    LatchController.
    '''

    def __init__(self,*args,**kwargs):
        pass

    def setStepper(self,stepper):
        self.stepper = stepper

    def setHomeSwitch(self,home_switch):
        self.home_switch = home_switch

class HeadFixationController():
    '''
    HeadFixationController.

    Example Usage:

    dev = HeadFixationController() # Might automatically find devices if available
    '''

    _PHIDGETS_CONFIGURATION_FILENAME = 'phidgets.json'

    def __init__(self,*args,**kwargs):
        if 'debug' in kwargs:
            self.debug = kwargs['debug']

        module_dir = os.path.split(__file__)[0]
        phidgets_configuration_path = os.path.join(module_dir,self._PHIDGETS_CONFIGURATION_FILENAME)
        print(phidgets_configuration_path)

        with open(phidgets_configuration_path) as f:
            phidgets_configuration_json = f.read()

        phidgets_configuration = json.loads(phidgets_configuration_json)

        self._phidgets = {}
        for name, phidget_configuration in phidgets_configuration.items():
            try:
                if (phidget_configuration['channel_class'] == 'DigitalInput'):
                    self._phidgets.update({name : DigitalInput()})
                    self._phidgets[name].setIsHubPortDevice(True)
                elif (phidget_configuration['channel_class'] == 'Stepper'):
                    self._phidgets.update({name : Stepper()})
                elif (phidget_configuration['channel_class'] == 'VoltageRatioInput'):
                    self._phidgets.update({name : VoltageRatioInput()})
                else:
                    break
                self._phidgets[name].name = name
                self._phidgets[name].configuration = phidget_configuration
                self._phidgets[name].setDeviceSerialNumber(phidget_configuration['device_serial_number'])
                self._phidgets[name].setHubPort(phidget_configuration['hub_port'])
                self._phidgets[name].setChannel(phidget_configuration['channel'])
                self._phidgets[name].setOnAttachHandler(self._phidget_attached)
                self._phidgets[name].open()
            except KeyError:
                break

        for name, phidget in self._phidgets.items():
            print(name, phidget.name, phidget.getAttached())

    def _phidget_attached(self,phidget):
        if phidget.configuration['channel_class'] == 'Stepper':
            print()
            phidget.setAcceleration(phidget.configuration['acceleration'])
            print(phidget.name,' acceleration: ',phidget.getAcceleration())
            phidget.setControlMode(phidget.configuration['control_mode'])
            print(phidget.name,' control_mode: ',phidget.getControlMode())
            phidget.setCurrentLimit(phidget.configuration['current_limit'])
            print(phidget.name,' current_limit: ',phidget.getCurrentLimit())
            phidget.setVelocityLimit(phidget.configuration['velocity_limit'])
            print(phidget.name,' velocity_limit: ',phidget.getVelocityLimit())
            # phidget.setEngaged(True)
            # print(phidget.name,' position: ',phidget.getPosition())
            # phidget.setTargetPosition(phidget.configuration['latch_position'])
            # print(phidget.name,' position: ',phidget.getPosition())
        elif phidget.configuration['channel_class'] == 'VoltageRatioInput':
            print('yes voltage thingy!')
            print(phidget.configuration)

    def all_phidgets_attached(self):
        for phidget in self._phidgets.values():
            if not phidget.getAttached():
                return False
        return True


# -----------------------------------------------------------------------------------------
if __name__ == '__main__':

    debug = False
    dev = HeadFixationController(debug=debug)
