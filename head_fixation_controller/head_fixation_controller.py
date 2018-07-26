import json
from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Net import *
from Phidget22.Devices.Stepper import *
from Phidget22.Devices.DigitalInput import *
from Phidget22.Devices.VoltageRatioInput import *
import os
from threading import Timer

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

class Latch():
    '''
    Latch.
    '''
    _CONTROL_MODE_STEP = 0
    _CONTROL_MODE_RUN = 1
    _HOME_SWITCH_ACTIVE = 0
    _POSITION_EPSILON = 2

    def __init__(self,*args,**kwargs):
        self._homed = False
        self._released_handler = None

    def set_stepper(self,stepper):
        self.stepper = stepper
        self.stepper.setOnStoppedHandler(self._stopped_handler)

    def set_home_switch(self,home_switch):
        self.home_switch = home_switch
        self.home_switch.setOnStateChangeHandler(self._home_switch_handler)

    def set_released_handler(self,released_handler):
        self._released_handler = released_handler

    def _all_attached(self):
        if not self.stepper.getAttached():
            return False
        if not self.home_switch.getAttached():
            return False
        return True

    def _stopped_handler(self,phidget):
        if self._at_release_position():
            if self._released_handler is not None:
                self._released_handler()

    def _at_home_position(self):
        position = self.stepper.getPosition()
        if abs(position) < self._POSITION_EPSILON:
            return True
        return False

    def _at_close_position(self):
        position = self.stepper.getPosition()
        if abs(position - self.stepper.configuration['close_position']) < self._POSITION_EPSILON:
            return True
        return False

    def _at_release_position(self):
        position = self.stepper.getPosition()
        if abs(position - self.stepper.configuration['release_position']) < self._POSITION_EPSILON:
            return True
        return False

    def _home_switch_handler(self,phidget,state):
        if state == self._HOME_SWITCH_ACTIVE:
            self._finish_homing()

    def _finish_homing(self):
        if not self._all_attached():
            return
        self.stop()
        self.stepper.setControlMode(self._CONTROL_MODE_STEP)
        self._zero()
        self.stepper.setVelocityLimit(self.stepper.configuration['velocity_limit'])
        self._homed = True
        if self._released_handler is not None:
            self._released_handler()

    def _zero(self):
        offset = self.stepper.getPosition()
        self.stepper.addPositionOffset(-offset)
        self.stepper.setTargetPosition(0)

    def home(self):
        if not self._all_attached():
            print("not all attached!")
            return
        if self.home_switch_active():
            self._finish_homing()
            self.stepper.setEngaged(True)
            return
        self.stepper.setEngaged(False)
        self._homed = False
        self.stepper.setControlMode(self._CONTROL_MODE_RUN)
        self.stepper.setVelocityLimit(self.stepper.configuration['home_velocity'])
        self.stepper.setEngaged(True)

    def homed(self):
        return self._homed

    def stop(self):
        self.stepper.setVelocityLimit(0)

    def close(self):
        if self.homed():
            if not self._at_close_position():
                self.stepper.setTargetPosition(self.stepper.configuration['close_position'])

    def release(self):
        if self.homed():
            if not self._at_release_position():
                self.stepper.setTargetPosition(self.stepper.configuration['release_position'])
        else:
            self.home()

    def home_switch_active(self):
        return self.home_switch.getState() == self._HOME_SWITCH_ACTIVE

    def released(self):
        if self._at_release_position():
            return True
        return False



class HeadFixationController():
    '''
    HeadFixationController.

    Example Usage:

    dev = HeadFixationController() # Might automatically find devices if available
    '''

    _PHIDGETS_CONFIGURATION_FILENAME = 'phidgets.json'
    _HEAD_BAR_SWITCH_ACTIVE = 1
    _RELEASE_SWITCH_ACTIVE = 1
    _SETUP_PERIOD = 1.0

    def __init__(self,*args,**kwargs):
        self._initialized = False
        if 'debug' in kwargs:
            self.debug = kwargs['debug']
        else:
            self.debug = DEBUG

        module_dir = os.path.split(__file__)[0]
        phidgets_configuration_path = os.path.join(module_dir,self._PHIDGETS_CONFIGURATION_FILENAME)

        with open(phidgets_configuration_path) as f:
            phidgets_configuration_json = f.read()

        phidgets_configuration = json.loads(phidgets_configuration_json)

        self._phidgets = {}
        for name, phidget_configuration in phidgets_configuration.items():
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

        self.right_head_latch = Latch()
        self.right_head_latch.set_stepper(self._phidgets['right_head_latch_motor'])
        self.right_head_latch.set_home_switch(self._phidgets['right_head_latch_home_switch'])
        self.right_head_latch.set_released_handler(self._latches_released_handler)

        self.left_head_latch = Latch()
        self.left_head_latch.set_stepper(self._phidgets['left_head_latch_motor'])
        self.left_head_latch.set_home_switch(self._phidgets['left_head_latch_home_switch'])
        self.left_head_latch.set_released_handler(self._latches_released_handler)

        self._phidgets['head_bar_switch'].setOnStateChangeHandler(self._head_bar_switch_handler)
        self._phidgets['release_switch'].setOnStateChangeHandler(self._release_switch_handler)

        self._setup_timer = Timer(self._SETUP_PERIOD,self._setup)
        self._setup_timer.start()

        self._initialized = True

    def _phidget_attached(self,phidget):
        if phidget.configuration['channel_class'] == 'Stepper':
            self._debug_print()
            phidget.setEngaged(False)
            phidget.setAcceleration(phidget.configuration['acceleration'])
            self._debug_print(phidget.name,' acceleration: ',phidget.getAcceleration())
            phidget.setCurrentLimit(phidget.configuration['current_limit'])
            self._debug_print(phidget.name,' current_limit: ',phidget.getCurrentLimit())
            phidget.setHoldingCurrentLimit(phidget.configuration['holding_current_limit'])
            self._debug_print(phidget.name,' holding_current_limit: ',phidget.getHoldingCurrentLimit())
            phidget.setVelocityLimit(phidget.configuration['velocity_limit'])
            self._debug_print(phidget.name,' velocity_limit: ',phidget.getVelocityLimit())
        elif phidget.configuration['channel_class'] == 'VoltageRatioInput':
            self._debug_print('yes voltage thingy!')
        elif phidget.configuration['channel_class'] == 'DigitalInput':
            self._debug_print('yes digital input thingy!')

    def _all_attached(self):
        for phidget in self._phidgets.values():
            if not phidget.getAttached():
                return False
        return True

    def _debug_print(self, *args):
        if self.debug:
            print(*args)

    def _setup(self):
        if self._initialized and self._all_attached():
            self.home_latches()
        else:
            self._setup_timer = Timer(self._SETUP_PERIOD,self._setup)
            self._setup_timer.start()

    def _dummy_switch_handler(self,phidget,state):
        pass

    def _head_bar_switch_handler(self,phidget,state):
        if state == self._HEAD_BAR_SWITCH_ACTIVE:
            self._debug_print('head bar switch activated')
            self.close_latches()

    def _release_switch_handler(self,phidget,state):
        if state == self._HEAD_BAR_SWITCH_ACTIVE:
            self._debug_print('release switch activated')
            self.release_latches()

    def _latches_released(self):
        return self.right_head_latch.released() and self.left_head_latch.released()

    def _latches_released_handler(self):
        if self._latches_released():
            self._debug_print('both latches released')
            self._phidgets['head_bar_switch'].setOnStateChangeHandler(self._head_bar_switch_handler)

    def home_latches(self):
        self._phidgets['head_bar_switch'].setOnStateChangeHandler(self._head_bar_switch_handler)
        self.right_head_latch.home()
        self.left_head_latch.home()

    def close_latches(self):
        self.right_head_latch.close()
        self.left_head_latch.close()

    def release_latches(self):
        if self.right_head_latch.homed() and self.left_head_latch.homed():
            self._phidgets['head_bar_switch'].setOnStateChangeHandler(self._dummy_switch_handler)
        self.right_head_latch.release()
        self.left_head_latch.release()


# -----------------------------------------------------------------------------------------
if __name__ == '__main__':

    debug = False
    dev = HeadFixationController(debug=debug)
