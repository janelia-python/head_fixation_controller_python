import sys
import time
import glob
import os
from tkinter import*
from Phidget22.Devices.Stepper import *
from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Net import *
from Phidget22.Devices.DigitalInput import *

try:
    from PhidgetHelperFunctions_lickport import *
    from PhidgetHelperFunctionsDI import *
except ImportError:
    sys.stderr.write("\nCould not find PhidgetHelperFunctions. Either add PhdiegtHelperFunctions.py to your project folder "
                      "or remove the import from your project.")
    sys.stderr.write("\nPress ENTER to end program.")
    readin = sys.stdin.readline()
    sys.exit()

'''
* Configures the device's DataInterval
* Displays info about the attached Phidget channel.  
* Fired when a Phidget channel with onAttachHandler registered attaches
*
* @param self The Phidget channel that fired the attach event
'''
def onAttachHandlerStepper(self):
    
    ph = self

    try:
        #If you are unsure how to use more than one Phidget channel with this event, we recommend going to
        #www.phidgets.com/docs/Using_Multiple_Phidgets for information
        
        print("\nAttach Event:")
        
        """
        * Get device information and display it.
        """
        channelClassName = ph.getChannelClassName()
        serialNumber = ph.getDeviceSerialNumber()
        channel = ph.getChannel()
        if(ph.getDeviceClass() == DeviceClass.PHIDCLASS_VINT):
            hubPort = ph.getHubPort()
            print("\n\t-> Channel Class: " + channelClassName + "\n\t-> Serial Number: " + str(serialNumber) +
                "\n\t-> Hub Port: " + str(hubPort) + "\n\t-> Channel:  " + str(channel) + "\n")
        else:
            print("\n\t-> Channel Class: " + channelClassName + "\n\t-> Serial Number: " + str(serialNumber) +
                    "\n\t-> Channel:  " + str(channel) + "\n")
    
        """
        * Set the DataInterval inside of the attach handler to initialize the device with this value.
        * DataInterval defines the minimum time between PositionChange events.
        * DataInterval can be set to any value from MinDataInterval to MaxDataInterval.
        """
        print("\tSetting DataInterval to 100 ms")
        try:
            ph.setDataInterval(100)
        except PhidgetException as e:
            sys.stderr.write("Runtime Error -> Setting DataInterval: \n\t")
            DisplayError(e)
            return
        
        """
        * Engage the Stepper inside of the attach handler to allow the motor to move to its target position
        * The motor will only track a target position if it is engaged.
        * Engaged can be set to True to enable the servo, or False to disable it.
        """
        print("\tEngaging Stepper")
        try:
            ph.setEngaged(True)
        except PhidgetException as e:
            sys.stderr.write("Runtime Error -> Setting Engaged: \n\t")
            DisplayError(e)
            return
        
    except PhidgetException as e:
        print("\nError in Attach Event:")
        DisplayError(e)
        traceback.print_exc()
        return

def onAttachHandlerDI(self):
    
    ph = self
    try:
        #If you are unsure how to use more than one Phidget channel with this event, we recommend going to
        #www.phidgets.com/docs/Using_Multiple_Phidgets for information
    
        print("\nAttach Event:")
        
        """
        * Get device information and display it.
        """
        serialNumber = ph.getDeviceSerialNumber()
        channelClass = ph.getChannelClassName()
        channel = ph.getChannel()
        
        deviceClass = ph.getDeviceClass()
        if (deviceClass != DeviceClass.PHIDCLASS_VINT):
            print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                  "\n\t-> Channel:  " + str(channel) + "\n")
        else:            
            hubPort = ph.getHubPort()
            print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                  "\n\t-> Hub Port: " + str(hubPort) + "\n\t-> Channel:  " + str(channel) + "\n")
        
    except PhidgetException as e:
        print("\nError in Attach Event:")
        DisplayError(e)
        traceback.print_exc()
        return


"""
* Displays info about the detached Phidget channel.
* Fired when a Phidget channel with onDetachHandler registered detaches
*
* @param self The Phidget channel that fired the attach event
"""
def onDetachHandler(self):

    ph = self

    try:
        #If you are unsure how to use more than one Phidget channel with this event, we recommend going to
        #www.phidgets.com/docs/Using_Multiple_Phidgets for information
        
        print("\nDetach Event:")
        
        """
        * Get device information and display it.
        """
        channelClassName = ph.getChannelClassName()
        serialNumber = ph.getDeviceSerialNumber()
        channel = ph.getChannel()
        if(ph.getDeviceClass() == DeviceClass.PHIDCLASS_VINT):
            hubPort = ph.getHubPort()
            print("\n\t-> Channel Class: " + channelClassName + "\n\t-> Serial Number: " + str(serialNumber) +
                "\n\t-> Hub Port: " + str(hubPort) + "\n\t-> Channel:  " + str(channel) + "\n")
        else:
            print("\n\t-> Channel Class: " + channelClassName + "\n\t-> Serial Number: " + str(serialNumber) +
                    "\n\t-> Channel:  " + str(channel) + "\n")
        
    except PhidgetException as e:
        print("\nError in Detach Event:")
        DisplayError(e)
        traceback.print_exc()
        return

"""
* Writes Phidget error info to stderr.
* Fired when a Phidget channel with onErrorHandler registered encounters an error in the library
*
* @param self The Phidget channel that fired the attach event
* @param errorCode the code associated with the error of enum type ph.ErrorEventCode
* @param errorString string containing the description of the error fired
"""
def onErrorHandler(self, errorCode, errorString):

    sys.stderr.write("[Phidget Error Event] -> " + errorString + " (" + str(errorCode) + ")\n")

"""
* Outputs the Stepper's most recently reported Position.
* Fired when a Stepper channel with onPositionChangeHandler registered meets DataInterval criteria
*
* @param self The Stepper channel that fired the PositionChange event
* @param Position The reported Position from the Stepper channel
"""
def onPositionChangeHandler(self, Position):

    #If you are unsure how to use more than one Phidget channel with this event, we recommend going to
    #www.phidgets.com/docs/Using_Multiple_Phidgets for information

    print("[Position Event] -> Position: " + str(Position))
    
"""
* Prints descriptions of how events related to this class work
"""
def PrintEventDescriptions():

    print("\n--------------------\n"
        "\n  | Position update events will call their associated function every time new Position data is received from the device.\n"
        "  | The rate of these events can be set by adjusting the DataInterval for the channel.\n"
        "  | Press ENTER once you have read this message.")
    readin = sys.stdin.readline(1)
    
    print("\n--------------------")

def get_line(filename,n):
    with open(filename, 'r') as f:
        for line_number, line in enumerate(f):
            if line_number == n:
                return line
                    
"""
* Creates, configures, and opens a Stepper channel.
* Provides interface for controlling TargetPosition of the Stepper.
* Closes out Stepper channel
*
* @return 0 if the program exits successfully, 1 if it exits with errors.
"""
def main0():
        
    try:
        """
        * Allocate a new Phidget Channel object
        """
        try:
            ch8 = Stepper()
            ch9 = Stepper()
            ch10 = Stepper()
            ch11 = DigitalInput()
            ch12 = DigitalInput()
            ch13 = DigitalInput()
        except PhidgetException as e:
            sys.stderr.write("Runtime Error -> Creating Stepper: \n\t")
            DisplayError(e)
            raise
        except RuntimeError as e:
            sys.stderr.write("Runtime Error -> Creating Stepper: \n\t" + e)
            raise

        """
        * Set matching parameters to specify which channel to open
        """
        #You may remove this line and hard-code the addressing parameters to fit your application
        """channelInfo = AskForDeviceParameters(ch)"""

        # setting motor
        'x axis'
        channelInfo8 = ChannelInfo()
        channelInfo8.deviceSerialNumber = 538380
        channelInfo8.hubPort            = 0
        channelInfo8.isHubPortDevice    = False
        channelInfo8.channel            = 0
        channelInfo8.isVint             = True
        channelInfo8.netInfo.isRemote   = False

        ch8.setDeviceSerialNumber(channelInfo8.deviceSerialNumber)
        ch8.setHubPort(channelInfo8.hubPort)
        ch8.setIsHubPortDevice(channelInfo8.isHubPortDevice)
        ch8.setChannel(channelInfo8.channel)

        'y axis'
        channelInfo9 = ChannelInfo()
        channelInfo9.deviceSerialNumber = 538380
        channelInfo9.hubPort            = 2
        channelInfo9.isHubPortDevice    = False
        channelInfo9.channel            = 0
        channelInfo9.isVint             = True
        channelInfo9.netInfo.isRemote   = False

        ch9.setDeviceSerialNumber(channelInfo9.deviceSerialNumber)
        ch9.setHubPort(channelInfo9.hubPort)
        ch9.setIsHubPortDevice(channelInfo9.isHubPortDevice)
        ch9.setChannel(channelInfo9.channel)

        'z axis'
        channelInfo10 = ChannelInfo()
        channelInfo10.deviceSerialNumber = 538380
        channelInfo10.hubPort            = 1
        channelInfo10.isHubPortDevice    = False
        channelInfo10.channel            = 0
        channelInfo10.isVint             = True
        channelInfo10.netInfo.isRemote   = False

        ch10.setDeviceSerialNumber(channelInfo10.deviceSerialNumber)
        ch10.setHubPort(channelInfo10.hubPort)
        ch10.setIsHubPortDevice(channelInfo10.isHubPortDevice)
        ch10.setChannel(channelInfo10.channel)

        # setting DI
        # setting front panel sensors 02042019
        # X limit
        channelInfo11 = ChannelInfo()
        channelInfo11.deviceSerialNumber = 538380
        channelInfo11.hubPort            = 4
        channelInfo11.isHubPortDevice    = True
        channelInfo11.channel            = 0
        channelInfo11.isVINT             = False
        channelInfo11.netInfo.isRemote   = False

        ch11.setDeviceSerialNumber(channelInfo11.deviceSerialNumber)
        ch11.setHubPort(channelInfo11.hubPort)
        ch11.setIsHubPortDevice(channelInfo11.isHubPortDevice)
        ch11.setChannel(channelInfo11.channel)
        
        # Y limit
        channelInfo12 = ChannelInfo()
        channelInfo12.deviceSerialNumber = 538380
        channelInfo12.hubPort            = 3
        channelInfo12.isHubPortDevice    = True
        channelInfo12.channel            = 0
        channelInfo12.isVINT             = True
        channelInfo12.netInfo.isRemote   = False

        ch12.setDeviceSerialNumber(channelInfo12.deviceSerialNumber)
        ch12.setHubPort(channelInfo12.hubPort)
        ch12.setIsHubPortDevice(channelInfo12.isHubPortDevice)
        ch12.setChannel(channelInfo12.channel)
        # Z limit
        channelInfo13 = ChannelInfo()
        channelInfo13.deviceSerialNumber = 538380
        channelInfo13.hubPort            = 5
        channelInfo13.isHubPortDevice    = True
        channelInfo13.channel            = 0
        channelInfo13.isVINT             = False
        channelInfo13.netInfo.isRemote   = False

        ch13.setDeviceSerialNumber(channelInfo13.deviceSerialNumber)
        ch13.setHubPort(channelInfo13.hubPort)
        ch13.setIsHubPortDevice(channelInfo13.isHubPortDevice)
        ch13.setChannel(channelInfo13.channel)

        """
        * Add ch11, 12 & 13 handlers before calling open so that no events are missed.
        """
        print("\n--------------------------------------")
        print("\nSetting OnAttachHandler...")
        ch11.setOnAttachHandler(onAttachHandlerDI)
        
        print("Setting OnDetachHandler...")
        ch11.setOnDetachHandler(onDetachHandler)

        print("\n--------------------------------------")
        print("\nSetting OnAttachHandler...")
        ch12.setOnAttachHandler(onAttachHandlerDI)
        
        print("Setting OnDetachHandler...")
        ch12.setOnDetachHandler(onDetachHandler)
        
       
        print("\n--------------------------------------")
        print("\nSetting OnAttachHandler...")
        ch13.setOnAttachHandler(onAttachHandlerDI)
        
        print("Setting OnDetachHandler...")
        ch13.setOnDetachHandler(onDetachHandler)

        
        
        """
        * Add Ch 8 9 10 event handlers before calling open so that no events are missed.
        """
        print("\n--------------------------------------")
        print("\nSetting OnAttachHandler...")
        ch8.setOnAttachHandler(onAttachHandlerStepper)
        ch9.setOnAttachHandler(onAttachHandlerStepper)
        ch10.setOnAttachHandler(onAttachHandlerStepper)
        
        print("Setting OnDetachHandler...")
        ch8.setOnDetachHandler(onDetachHandler)
        ch9.setOnDetachHandler(onDetachHandler)
        ch10.setOnDetachHandler(onDetachHandler)
        
        print("Setting OnErrorHandler...")
        ch8.setOnErrorHandler(onErrorHandler)
        ch9.setOnErrorHandler(onErrorHandler)
        ch10.setOnErrorHandler(onErrorHandler)

        #This call may be harmlessly removed
        PrintEventDescriptions()
        
        print("\nSetting OnPositionChangeHandler...")
        ch8.setOnPositionChangeHandler(onPositionChangeHandler)
        ch9.setOnPositionChangeHandler(onPositionChangeHandler)
        ch10.setOnPositionChangeHandler(onPositionChangeHandler)
        
        """
        * Open the channel with a timeout
        """
        print("\nOpening and Waiting for Attachment...")
        
        try:
            ch8.openWaitForAttachment(5000)
            ch9.openWaitForAttachment(5000)
            ch10.openWaitForAttachment(5000)
            ch11.openWaitForAttachment(5000)
            ch12.openWaitForAttachment(5000)
            ch13.openWaitForAttachment(5000)
        except PhidgetException as e:
            PrintOpenErrorMessage(e, ch8)
            raise EndProgramSignal("Program Terminated: Open Failed")

        print("--------------------\n"
        "\n  | Stepper motor position can be controlled by setting its Target Position.\n"
        "  | The target position can be a number between MinPosition and MaxPosition.\n"
        "  | For this example, acceleration and velocity limit are left as their default values, but can be changed in custom code.\n"

        "\nInput a desired position and press ENTER\n"
        "Input Q and press ENTER to quit\n")

        """
        * Set parameters of stepper
        """
        ch8.setAcceleration(20002)
        ch9.setAcceleration(20002)
        ch10.setAcceleration(20002)
        
        Acc_lickport = ch8.getAcceleration()
        print(Acc_lickport)

        ch8.setCurrentLimit(0.1)
        ch9.setCurrentLimit(0.145)
        ch10.setCurrentLimit(0.1)
        Cl_lickport = ch8.getCurrentLimit()
        print(Cl_lickport)

        ch8.setVelocityLimit(575)
        ch9.setVelocityLimit(575)
        ch10.setVelocityLimit(575)
        Vel_lickport = ch8.getVelocityLimit()
        print(Vel_lickport)

        ch8.setHoldingCurrentLimit(0)
        ch9.setHoldingCurrentLimit(0)
        ch10.setHoldingCurrentLimit(0)
        


        # Detect moving limit in x, y, and z axis
    
        ch11Stat = ch11.getState()
        ch12Stat = ch12.getState()
        ch13Stat = ch13.getState()
                

    except PhidgetException as e:
        sys.stderr.write("\nExiting with error(s)...")
        DisplayError(e)
        traceback.print_exc()
        print("Cleaning up...")
        #clear the PositionChange event handler 
        ch8.setOnPositionChangeHandler(None)  
        ch8.close()
        ch9.setOnPositionChangeHandler(None)  
        ch9.close()
        ch10.setOnPositionChangeHandler(None)  
        ch10.close()
        return 1
    except EndProgramSignal as e:
        print(e)
        print("Cleaning up...")
        #clear the PositionChange event handler 
        ch8.setOnPositionChangeHandler(None)  
        ch8.close()
        ch9.setOnPositionChangeHandler(None)  
        ch9.close()
        ch10.setOnPositionChangeHandler(None)  
        ch10.close()
        return 1
   
     

    """
    Try zero X
    """
    def zero():
        global X_home_position, Y_home_position, Z_home_position     
        print('Zeroing now!')

        ch12Stat = ch12.getState()
        while ch12Stat ==1:
            Y = ch9.getPosition() - 10
            ch9.setTargetPosition(Y)
            ch12Stat = ch12.getState()
        
        ch11Stat = ch11.getState()
        while ch11Stat ==1:
            X = ch8.getPosition() - 10
            ch8.setTargetPosition(X)
            ch11Stat = ch11.getState()        
            
        ch13Stat = ch13.getState()    
        while ch13Stat ==1:
            Z = ch10.getPosition() - 10
            ch10.setTargetPosition(Z)
            ch13Stat = ch13.getState()
            
        X_home_position = 0-ch8.getPosition()
        Y_home_position = 0-ch9.getPosition()
        Z_home_position = 0-ch10.getPosition()
        
            
    zero()
    print("Cleaning up...")
    ch8.setOnPositionChangeHandler(None)  
    ch8.close()
    ch9.setOnPositionChangeHandler(None)  
    ch9.close()
    ch10.setOnPositionChangeHandler(None)  
    ch10.close()  # deatch and the re-attach so that the stepper motor will start at the same home position


    try:
        """
        * Allocate a new Phidget Channel object
        """
        try:
            ch8 = Stepper()
            ch9 = Stepper()
            ch10 = Stepper()
            ch11 = DigitalInput()
            ch12 = DigitalInput()
            ch13 = DigitalInput()
        except PhidgetException as e:
            sys.stderr.write("Runtime Error -> Creating Stepper: \n\t")
            DisplayError(e)
            raise
        except RuntimeError as e:
            sys.stderr.write("Runtime Error -> Creating Stepper: \n\t" + e)
            raise

        """
        * Set matching parameters to specify which channel to open
        """
        #You may remove this line and hard-code the addressing parameters to fit your application
        """channelInfo = AskForDeviceParameters(ch)"""

        # setting motor
        'x axis'
        channelInfo8 = ChannelInfo()
        channelInfo8.deviceSerialNumber = 538380
        channelInfo8.hubPort            = 0
        channelInfo8.isHubPortDevice    = False
        channelInfo8.channel            = 0
        channelInfo8.isVint             = True
        channelInfo8.netInfo.isRemote   = False

        ch8.setDeviceSerialNumber(channelInfo8.deviceSerialNumber)
        ch8.setHubPort(channelInfo8.hubPort)
        ch8.setIsHubPortDevice(channelInfo8.isHubPortDevice)
        ch8.setChannel(channelInfo8.channel)

        'y axis'
        channelInfo9 = ChannelInfo()
        channelInfo9.deviceSerialNumber = 538380
        channelInfo9.hubPort            = 2
        channelInfo9.isHubPortDevice    = False
        channelInfo9.channel            = 0
        channelInfo9.isVint             = True
        channelInfo9.netInfo.isRemote   = False

        ch9.setDeviceSerialNumber(channelInfo9.deviceSerialNumber)
        ch9.setHubPort(channelInfo9.hubPort)
        ch9.setIsHubPortDevice(channelInfo9.isHubPortDevice)
        ch9.setChannel(channelInfo9.channel)

        'z axis'
        channelInfo10 = ChannelInfo()
        channelInfo10.deviceSerialNumber = 538380
        channelInfo10.hubPort            = 1
        channelInfo10.isHubPortDevice    = False
        channelInfo10.channel            = 0
        channelInfo10.isVint             = True
        channelInfo10.netInfo.isRemote   = False

        ch10.setDeviceSerialNumber(channelInfo10.deviceSerialNumber)
        ch10.setHubPort(channelInfo10.hubPort)
        ch10.setIsHubPortDevice(channelInfo10.isHubPortDevice)
        ch10.setChannel(channelInfo10.channel)

        # setting DI
        # setting front panel sensors 02042019
        # X limit
        channelInfo11 = ChannelInfo()
        channelInfo11.deviceSerialNumber = 538380
        channelInfo11.hubPort            = 4
        channelInfo11.isHubPortDevice    = True
        channelInfo11.channel            = 0
        channelInfo11.isVINT             = False
        channelInfo11.netInfo.isRemote   = False

        ch11.setDeviceSerialNumber(channelInfo11.deviceSerialNumber)
        ch11.setHubPort(channelInfo11.hubPort)
        ch11.setIsHubPortDevice(channelInfo11.isHubPortDevice)
        ch11.setChannel(channelInfo11.channel)
        
        # Y limit
        channelInfo12 = ChannelInfo()
        channelInfo12.deviceSerialNumber = 538380
        channelInfo12.hubPort            = 3
        channelInfo12.isHubPortDevice    = True
        channelInfo12.channel            = 0
        channelInfo12.isVINT             = False
        channelInfo12.netInfo.isRemote   = False

        ch12.setDeviceSerialNumber(channelInfo12.deviceSerialNumber)
        ch12.setHubPort(channelInfo12.hubPort)
        ch12.setIsHubPortDevice(channelInfo12.isHubPortDevice)
        ch12.setChannel(channelInfo12.channel)
        # Z limit
        channelInfo13 = ChannelInfo()
        channelInfo13.deviceSerialNumber = 538380
        channelInfo13.hubPort            = 5
        channelInfo13.isHubPortDevice    = True
        channelInfo13.channel            = 0
        channelInfo13.isVINT             = False
        channelInfo13.netInfo.isRemote   = False

        ch13.setDeviceSerialNumber(channelInfo13.deviceSerialNumber)
        ch13.setHubPort(channelInfo13.hubPort)
        ch13.setIsHubPortDevice(channelInfo13.isHubPortDevice)
        ch13.setChannel(channelInfo13.channel)

        """
        * Add ch11, 12 & 13 handlers before calling open so that no events are missed.
        """
        print("\n--------------------------------------")
        print("\nSetting OnAttachHandler...")
        ch11.setOnAttachHandler(onAttachHandlerDI)
        
        print("Setting OnDetachHandler...")
        ch11.setOnDetachHandler(onDetachHandler)

        print("\n--------------------------------------")
        print("\nSetting OnAttachHandler...")
        ch12.setOnAttachHandler(onAttachHandlerDI)
        
        print("Setting OnDetachHandler...")
        ch12.setOnDetachHandler(onDetachHandler)
        
       
        print("\n--------------------------------------")
        print("\nSetting OnAttachHandler...")
        ch13.setOnAttachHandler(onAttachHandlerDI)
        
        print("Setting OnDetachHandler...")
        ch13.setOnDetachHandler(onDetachHandler)

        
        
        """
        * Add Ch 8 9 10 event handlers before calling open so that no events are missed.
        """
        print("\n--------------------------------------")
        print("\nSetting OnAttachHandler...")
        ch8.setOnAttachHandler(onAttachHandlerStepper)
        ch9.setOnAttachHandler(onAttachHandlerStepper)
        ch10.setOnAttachHandler(onAttachHandlerStepper)
        
        print("Setting OnDetachHandler...")
        ch8.setOnDetachHandler(onDetachHandler)
        ch9.setOnDetachHandler(onDetachHandler)
        ch10.setOnDetachHandler(onDetachHandler)
        
        print("Setting OnErrorHandler...")
        ch8.setOnErrorHandler(onErrorHandler)
        ch9.setOnErrorHandler(onErrorHandler)
        ch10.setOnErrorHandler(onErrorHandler)

        #This call may be harmlessly removed
        PrintEventDescriptions()
        
        print("\nSetting OnPositionChangeHandler...")
        ch8.setOnPositionChangeHandler(onPositionChangeHandler)
        ch9.setOnPositionChangeHandler(onPositionChangeHandler)
        ch10.setOnPositionChangeHandler(onPositionChangeHandler)
        
        """
        * Open the channel with a timeout
        """
        print("\nOpening and Waiting for Attachment...")
        
        try:
            ch8.openWaitForAttachment(5000)
            ch9.openWaitForAttachment(5000)
            ch10.openWaitForAttachment(5000)
            ch11.openWaitForAttachment(5000)
            ch12.openWaitForAttachment(5000)
            ch13.openWaitForAttachment(5000)
        except PhidgetException as e:
            PrintOpenErrorMessage(e, ch8)
            raise EndProgramSignal("Program Terminated: Open Failed")

        print("--------------------\n"
        "\n  | Stepper motor position can be controlled by setting its Target Position.\n"
        "  | The target position can be a number between MinPosition and MaxPosition.\n"
        "  | For this example, acceleration and velocity limit are left as their default values, but can be changed in custom code.\n"

        "\nInput a desired position and press ENTER\n"
        "Input Q and press ENTER to quit\n")

        """
        * Set parameters of stepper
        """
        ch8.setAcceleration(20002)
        ch9.setAcceleration(20002)
        ch10.setAcceleration(20002)
        
        Acc_lickport = ch8.getAcceleration()
        print(Acc_lickport)

        ch8.setCurrentLimit(0.1)
        ch9.setCurrentLimit(0.145)
        ch10.setCurrentLimit(0.1)
        Cl_lickport = ch8.getCurrentLimit()
        print(Cl_lickport)

        ch8.setVelocityLimit(575)
        ch9.setVelocityLimit(575)
        ch10.setVelocityLimit(575)
        Vel_lickport = ch8.getVelocityLimit()
        print(Vel_lickport)

        ch8.setHoldingCurrentLimit(0)
        ch9.setHoldingCurrentLimit(0)
        ch10.setHoldingCurrentLimit(0)
        


        # Detect moving limit in x, y, and z axis
    
        ch11Stat = ch11.getState()
        ch12Stat = ch12.getState()
        ch13Stat = ch13.getState()
                

    except PhidgetException as e:
        sys.stderr.write("\nExiting with error(s)...")
        DisplayError(e)
        traceback.print_exc()
        print("Cleaning up...")
        #clear the PositionChange event handler 
        ch8.setOnPositionChangeHandler(None)  
        ch8.close()
        ch9.setOnPositionChangeHandler(None)  
        ch9.close()
        ch10.setOnPositionChangeHandler(None)  
        ch10.close()
        return 1
    except EndProgramSignal as e:
        print(e)
        print("Cleaning up...")
        #clear the PositionChange event handler 
        ch8.setOnPositionChangeHandler(None)  
        ch8.close()
        ch9.setOnPositionChangeHandler(None)  
        ch9.close()
        ch10.setOnPositionChangeHandler(None)  
        ch10.close()
        return 1
   
    def X_left():
        global ch11Stat
        try:
            ch11Stat = ch11.getState()
            if ch11Stat ==0:
                X_state.config(text = "YES!")
            elif ch11Stat ==1:
                X_state.config(text = "No!!")
            X_target = ch8.getPosition() + 100
            ch8.setTargetPosition(X_target)
            X_label.config(text = 'X position = ' + str(ch8.getPosition()+100))
            X_move = ch8.getPosition()+100
            Y_move = ch9.getPosition()
            Z_move = ch10.getPosition()
            with open(path+Name,"w") as f:
                f.write('%d' % X_move + ' %d' % Y_move + ' %d' % Z_move)
        except:
            X_label.config(text = "X position = " + str(ch8.getPosition()+100))
            

    def X_right():
        global ch11Stat
        try:
            ch11Stat = ch11.getState()
            if ch11Stat ==0:
                X_state.config(text = "YES!")
            elif ch11Stat ==1:
                X_state.config(text = "No!!")
            X_target = ch8.getPosition() - 100
            ch8.setTargetPosition(X_target)
            X_label.config(text = 'X position = ' + str(ch8.getPosition()-100))
            X_move = ch8.getPosition()-100
            Y_move = ch9.getPosition()
            Z_move = ch10.getPosition()
            with open(path+Name,"w") as f:
                f.write('%d' % X_move + ' %d' % Y_move + ' %d' % Z_move)
        except:
            X_label.config(text = 'X position = ' + str(ch8.getPosition()-100))

##    def X_home():
##        global X_home_position
##        X_home_position = 0-ch8.getPosition()
##        X_label.config(text = 'X position = ' + str(ch8.getPosition()+X_home_position))

    def X_target():
        global ent_X
        string = ent_X.get()

        X_targetPosition = float(string)
        ch8.setTargetPosition(X_targetPosition)
        X_label.config(text = 'X position = ' + str(string))
        X_move = X_targetPosition
        Y_move = ch9.getPosition()
        Z_move = ch10.getPosition()
        with open(path+Name,"w") as f:
            f.write('%d' % X_move + ' %d' % Y_move + ' %d' % Z_move)
##        except:
##            X_targetPosition = float(string)
##            ch8.setTargetPosition(X_targetPosition)
##            X_label.config(text = 'X position = ' + str(string))
            

    def Y_forward():
        global ch12Stat
        try:
            ch12Stat = ch12.getState()
            if ch12Stat ==0:
                Y_state.config(text = "YES!")
            elif ch12Stat ==1:
                Y_state.config(text = "No!!")
            Y_target = ch9.getPosition() + 100
            ch9.setTargetPosition(Y_target)
            Y_label.config(text = 'Y position = ' + str(ch9.getPosition()+100))
            X_move = ch8.getPosition()
            Y_move = ch9.getPosition()+100
            Z_move = ch10.getPosition()
            with open(path+Name,"w") as f:
                f.write('%d' % X_move + ' %d' % Y_move + ' %d' % Z_move)
        except:
            Y_label.config(text = "Y position = " + str(ch9.getPosition()+100))

    def Y_backward():
        global ch12Stat
        try:
            ch12Stat = ch12.getState()
            if ch12Stat ==0:
                Y_state.config(text = "YES!")
            elif ch12Stat ==1:
                Y_state.config(text = "No!!")
            Y_target = ch9.getPosition() - 100
            ch9.setTargetPosition(Y_target)
            Y_label.config(text = 'Y position = ' + str(ch9.getPosition()-100))
            X_move = ch8.getPosition()
            Y_move = ch9.getPosition()-100
            Z_move = ch10.getPosition()
            with open(path+Name,"w") as f:
                f.write('%d' % X_move + ' %d' % Y_move + ' %d' % Z_move)
        except:
            Y_label.config(text = 'Y position = ' + str(ch9.getPosition()-100))


##    def Y_home():
##        global Y_home_position
##        Y_home_position = 0-ch9.getPosition()
##        Y_label.config(text = 'Y position = ' + str(ch9.getPosition()+Y_home_position))

    def Y_target():
        global ent_Y
        string = ent_Y.get()
        
        Y_targetPosition = float(string)
        ch9.setTargetPosition(Y_targetPosition)
        Y_label.config(text = 'Y position = ' + str(string))
        X_move = ch8.getPosition()
        Y_move = Y_targetPosition
        Z_move = ch10.getPosition()
        with open(path+Name,"w") as f:
            f.write('%d' % X_move + ' %d' % Y_move + ' %d' % Z_move)
        

    def Z_down():
        global ch13Stat
        try:
            ch13Stat = ch13.getState()
            if ch13Stat ==0:
                Z_state.config(text = "YES!")
            elif ch13Stat ==1:
                Z_state.config(text = "No!!")
            Z_target = ch10.getPosition() + 100
            ch10.setTargetPosition(Z_target)
            Z_label.config(text = 'Z position = ' + str(ch10.getPosition()+100))
            X_move = ch8.getPosition()
            Y_move = ch9.getPosition()
            Z_move = ch10.getPosition()+100
            with open(path+Name,"w") as f:
                f.write('%d' % X_move + ' %d' % Y_move + ' %d' % Z_move)
        except:
            Z_label.config(text = "Z position = " + str(ch10.getPosition()+100))

    def Z_up():
        global ch13Stat
        try:
            ch13Stat = ch13.getState()
            if ch13Stat ==0:
                Z_state.config(text = "YES!")
            elif ch13Stat ==1:
                Z_state.config(text = "No!!")
            Z_target = ch10.getPosition() - 100
            ch10.setTargetPosition(Z_target)
            Z_label.config(text = 'Z position = ' + str(ch10.getPosition()-100))
            X_move = ch8.getPosition()
            Y_move = ch9.getPosition()
            Z_move = ch10.getPosition()-100
            with open(path+Name,"w") as f:
                f.write('%d' % X_move + ' %d' % Y_move + ' %d' % Z_move)
        except:
            Z_label.config(text = 'Z position = ' + str(ch10.getPosition()-100))

##    def Z_home():
##        global Z_home_position
##        Z_home_position = 0-ch10.getPosition()
##        Z_label.config(text = 'Z position = ' + str(ch10.getPosition()+Z_home_position))

    def Z_target():
        global ent_Z
        string = ent_Z.get()
        
        Z_targetPosition = float(string)
        ch10.setTargetPosition(Z_targetPosition)
        Z_label.config(text = 'Z position = ' + str(string))
        X_move = ch8.getPosition()
        Y_move = ch9.getPosition()
        Z_move = Z_targetPosition
        with open(path+Name,"w") as f:
            f.write('%d' % X_move + ' %d' % Y_move + ' %d' % Z_move)
        
        

    def X_axis(parent):
        global X_label, ent_X, X_state, ch11Stat
        X_label = Label(parent,text = "X position ")
        X_label.grid(row = 1, column = 2)
        ch11Stat = ch11.getState()
        X_state = Label(parent,text = "No!!")
        X_state.grid(row = 2, column = 0, sticky = NSEW)
        X_state.config(bg = "black", fg = "pink")
        #Button(parent,text = "Zero X",command = X_home).grid(row = 2, column = 1,sticky = NSEW)
        Button(parent,text = "Left", command = X_right).grid(row = 2, column = 2,sticky = NSEW)
        Button(parent,text = "Right", command = X_left).grid(row = 2, column = 3,sticky = NSEW)
        ent_X = Entry(parent)
        ent_X.insert(0, 'Type target position')
        ent_X.grid(row=2, column=4, columnspan=60)
        Button(parent,text = "OK", command = X_target).grid(row = 2, column = 65, sticky = NSEW)

    def Y_axis(parent):
        global Y_label, ent_Y, Y_state, ch12Stat
        Y_label = Label(parent,text = "Y position")
        Y_label.grid(row = 3, column = 2)
        ch12Stat = ch12.getState()
        Y_state = Label(parent,text = "No!!")
        Y_state.grid(row = 4, column = 0, sticky = NSEW)
        Y_state.config(bg = "black", fg = "pink")
        #Button(parent,text = "Zero Y",command = Y_home).grid(row = 4, column = 1,sticky = NSEW)
        Button(parent,text = "Backward", command = Y_backward).grid(row = 4, column = 3,sticky = NSEW)
        Button(parent,text = "Forward", command = Y_forward).grid(row = 4, column = 2,sticky = NSEW)
        ent_Y = Entry(parent)
        ent_Y.insert(0, 'Type target position')
        ent_Y.grid(row=4, column=4, columnspan=60)
        Button(parent,text = "OK", command = Y_target).grid(row = 4, column = 65, sticky = NSEW)

    def Z_axis(parent):
        global Z_label, ent_Z, Z_state, ch13Stat
        Z_label = Label(parent,text = "Z position")
        Z_label.grid(row = 5, column = 2)
        ch13Stat = ch13.getState()
        Z_state = Label(parent,text = "No!!")
        Z_state.grid(row = 6, column = 0, sticky = NSEW)
        Z_state.config(bg = "black", fg = "pink")
        #Button(parent,text = "Zero Z",command = Z_home).grid(row = 6, column = 1,sticky = NSEW)
        Button(parent,text = "Up", command = Z_up).grid(row = 6, column = 2,sticky = NSEW)
        Button(parent,text = "Down", command = Z_down).grid(row = 6, column = 3,sticky = NSEW)
        ent_Z = Entry(parent)
        ent_Z.insert(0, 'Type target position')
        ent_Z.grid(row=6, column=4, columnspan=60)
        Button(parent,text = "OK", command = Z_target).grid(row = 6, column = 65, sticky = NSEW)

    MouseName = input("Please type the mouse name :  ")
    Date = input("Please type the date today (yyyymmdd) :  ")
    
    try:
        list_of_files = glob.glob('C:/Users/labadmin/Documents/Python/Lickport_position/{0}/*'.format(MouseName)) # * means all if need specific format then *.csv
        latest_file = max(list_of_files, key=os.path.getctime) # find the most recent text file
        fileHandle = open(latest_file,"r" )
        lineList = fileHandle.readlines()
        fileHandle.close()
        resultX = []
        resultY = []
        resultZ = []

        for x in lineList: # load previous x, y, z location: last line
            resultX.append(x.split(' ')[0])
            X_previous = float(resultX[-1])  # first column in the last line
            resultY.append(x.split(' ')[1])
            Y_previous = float(resultY[-1])  # second column in the last line
            resultZ.append(x.split(' ')[2])
            Z_previous = float(resultZ[-1])  # third column in the last line
            
        X_targetPosition = ch8.getPosition()+X_previous        
        ch8.setTargetPosition(X_targetPosition)
        #X_label.config(text = 'X position = ' + str(string))    
    
        Y_targetPosition = ch9.getPosition()+Y_previous       
        ch9.setTargetPosition(Y_targetPosition)
        #Y_label.config(text = 'Y position = ' + str(string))
    
        Z_targetPosition = ch10.getPosition()+Z_previous        
        ch10.setTargetPosition(Z_targetPosition)
        #Z_label.config(text = 'Z position = ' + str(string))
               
    except:
        os.makedirs('C:/Users/labadmin/Documents/Python/Lickport_position/{0}/'.format(MouseName))
        
        X_targetPosition = ch8.getPosition()+1800        
        ch8.setTargetPosition(X_targetPosition)
        X_previous = 1800
        #X_label.config(text = 'X position = ' + str(string))    
    
        Y_targetPosition = ch9.getPosition()+6400       
        ch9.setTargetPosition(Y_targetPosition)
        Y_previous = 6400
        #Y_label.config(text = 'Y position = ' + str(string))
    
        Z_targetPosition = ch10.getPosition()+1490        
        ch10.setTargetPosition(Z_targetPosition)
        Z_previous = 1490
        #Z_label.config(text = 'Z position = ' + str(string))
        
        

    Name = MouseName + '_' + Date +'.txt'
    path = 'C:/Users/labadmin/Documents/Python/Lickport_position/{0}/'.format(MouseName)
    f = open(path+Name,"w") # create the new text file
    X_start = ch8.getPosition()+X_previous
    Y_start = ch9.getPosition()+Y_previous
    Z_start = ch10.getPosition()+Z_previous    
    f.write('%d' % X_start + ' %d' % Y_start + ' %d' % Z_start) # write starting location
    f.close()
    print('la')
    
    motor = Tk()
    frm = Frame(motor)
    frm.pack()
    X_axis(frm)
    Y_axis(frm)
    Z_axis(frm)
    motor.title('lickport controller')

    ## Read lickport text file every 1.5 sec ##
    def read_lickport():        
        global X_recent,Y_recent,Z_recent
        fid = open(path+Name,"r")
        recent = fid.readlines()
        fid.close()
        recentX = []
        recentY = []
        recentZ = []        
        for x in recent: # load recent x, y, z location: last line
                recentX.append(x.split(' ')[0])
                X_recent = float(recentX[-1])  # first column in the last line
                recentY.append(x.split(' ')[1])
                Y_recent = float(recentY[-1])  # second column in the last line
                recentZ.append(x.split(' ')[2])
                Z_recent = float(recentZ[-1])  # third column in the last line        
        motor.after(1500,read_lickport)
        X_targetPositionRecent = X_recent        
        ch8.setTargetPosition(X_targetPositionRecent)
        Y_targetPositionRecent = Y_recent         
        ch9.setTargetPosition(Y_targetPositionRecent)
        Z_targetPositionRecent = Z_recent         
        ch10.setTargetPosition(Z_targetPositionRecent)


    motor.after(1500, read_lickport)    #update lickport position every 1.5 sec
    motor.mainloop()
    

main0()



