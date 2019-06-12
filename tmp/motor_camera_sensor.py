import sys
import os
import time
from datetime import datetime
import numpy as np
import cv2
import traceback
import math
from Phidget22.Devices.DigitalInput import *
from Phidget22.Devices.VoltageRatioInput import *
from Phidget22.Devices.DigitalOutput import *
from Phidget22.Devices.Stepper import *
from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Net import *

try:
    from PhidgetHelperFunctions import *
    from PhidgetHelperFunctionsDI import *
    from PhidgetHelperFunctionsDO import *
    from PhidgetHelperFunctionsStepper import *
except ImportError:
    sys.stderr.write("\nCould not find PhidgetHelperFunctions. Either add PhdiegtHelperFunctions.py to your project folder "
                     "or remove the import from your project.")
    sys.stderr.write("\nPress ENTER to end program.")
    readin = sys.stdin.readline()
    sys.exit()

"""
* Configures the device's DataInterval and ChangeTrigger.
* Displays info about the attached phidget channel.
* Fired when a Phidget channel with onAttachHandler registered attaches
*
* @param self The Phidget channel that fired the attach event
"""
def onAttachHandler(self):
    
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
                "\n\t-> Hub Port: " + str(hubPort) + "\n\t-> Channel " + str(channel) + "\n")
        else:
            print("\n\t-> Channel Class: " + channelClassName + "\n\t-> Serial Number: " + str(serialNumber) +
                    "\n\t-> Channel " + str(channel) + "\n")

   
        """
        * Set the DataInterval inside of the attach handler to initialize the device with this value.
        * DataInterval defines the minimum time between VoltageRatioChange events.
        * DataInterval can be set to any value from MinDataInterval to MaxDataInterval.
        """
        print("\n\tSetting DataInterval to 100ms")
        ph.setDataInterval(100)

        """
        * Set the VoltageRatioChangeTrigger inside of the attach handler to initialize the device with this value.
        * VoltageRatioChangeTrigger will affect the frequency of VoltageRatioChange events, by limiting them to only occur when
        * the voltage ratio changes by at least the value set.
        """
        print("\tSetting Voltage Ratio ChangeTrigger to 0.0")
        ph.setVoltageRatioChangeTrigger(0.0)
        
        """
        * Set the SensorType inside of the attach handler to initialize the device with this value.
        * You can find the appropriate SensorType for your sensor in its User Guide and the VoltageRatioInput API
        * SensorType will apply the appropriate calculations to the voltage ratio reported by the device
        * to convert it to the sensor's units.
        * SensorType can only be set for Sensor Port voltage ratio inputs (VINT Ports and Analog Input Ports)
        """
        if(ph.getChannelSubclass() == ChannelSubclass.PHIDCHSUBCLASS_VOLTAGERATIOINPUT_SENSOR_PORT):
            print("\tSetting VoltageRatio SensorType")
            ph.setSensorType(VoltageRatioSensorType.SENSOR_TYPE_VOLTAGERATIO)
            
        
    except PhidgetException as e:
        print("\nError in Attach Event:")
        DisplayError(e)
        traceback.print_exc()
        return

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
        print("\tSetting DataInterval to 1000ms")
        try:
            ph.setDataInterval(1000)
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
* Displays info about the detached phidget channel.
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
                "\n\t-> Hub Port: " + str(hubPort) + "\n\t-> Channel " + str(channel) + "\n")
        else:
            print("\n\t-> Channel Class: " + channelClassName + "\n\t-> Serial Number: " + str(serialNumber) +
                    "\n\t-> Channel " + str(channel) + "\n")
        
    except PhidgetException as e:
        print("\nError in Detach Event:")
        DisplayError(e)
        traceback.print_exc()
        return


"""
* Writes phidget error info to stderr.
* Fired when a Phidget channel with onErrorHandler registered encounters an error in the library
*
* @param self The Phidget channel that fired the attach event
* @param errorCode the code associated with the error of enum type ph.ErrorEventCode
* @param errorString string containing the description of the error fired
"""
def onErrorHandler(self, errorCode, errorString):

    sys.stderr.write("[Phidget Error Event] -> " + errorString + " (" + str(errorCode) + ")\n")

def PrintEventDescriptions():

    print("\n--------------------\n"
        "\n  | Voltage Ratio change events will call their associated function every time new voltage ratio data is received from the device.\n"
        "  | The rate of these events can be set by adjusting the DataInterval for the channel.\n")
        
    print(
        "\n  | Sensor change events contain the most recent sensor value received from the device.\n"
        "  | Sensor change events will occur instead of Voltage Ratio change events if the SensorType is changed from the default.\n"
        "  | Press ENTER once you have read this message.")
    readin = sys.stdin.readline(1)
    
    print("\n--------------------")


"""
* Creates, configures, and opens a VoltageRatioInput channel.
* Displays Voltage Ratio events for 10 seconds
* Closes out VoltageRatioInput channel
*
* @return 0 if the program exits successfully, 1 if it exits with errors.
"""
def main():
    try:    
        try:
            ch = VoltageRatioInput()
            ch2 = DigitalInput()
            ch3 = DigitalInput()
            ch4 = DigitalOutput()
            ch5 = Stepper()
            ch6 = Stepper()
            ch7 = DigitalInput()
        except PhidgetException as e:
            sys.stderr.write("Runtime Error -> Creating VoltageRatioInput: \n\t")
            DisplayError(e)
            raise
        except RuntimeError as e:
            sys.stderr.write("Runtime Error -> Creating VoltageRatioInput: \n\t" + e)
            raise

        """
        * Set matching parameters to specify which channel to open
        """

        # setting hard coded 081418
        channelInfo = ChannelInfo()
        channelInfo.deviceSerialNumber = 527115
        channelInfo.hubPort            = 0
        channelInfo.isHubPortDevice    = False
        channelInfo.channel            = 0
        channelInfo.isVINT             = True
        channelInfo.netInfo.isRemote   = False
        
        ch.setDeviceSerialNumber(channelInfo.deviceSerialNumber)
        ch.setHubPort(channelInfo.hubPort)
        ch.setIsHubPortDevice(channelInfo.isHubPortDevice)
        ch.setChannel(channelInfo.channel)

        #setting front panel sensors 082718
        channelInfo2 = ChannelInfo()
        channelInfo2.deviceSerialNumber = 527115
        channelInfo2.hubPort            = 2
        channelInfo2.isHubPortDevice    = True
        channelInfo2.channel            = 0
        channelInfo2.isVINT             = False
        channelInfo2.netInfo.isRemote   = False

        ch2.setDeviceSerialNumber(channelInfo2.deviceSerialNumber)
        ch2.setHubPort(channelInfo2.hubPort)
        ch2.setIsHubPortDevice(channelInfo2.isHubPortDevice)
        ch2.setChannel(channelInfo2.channel)

        channelInfo3 = ChannelInfo()
        channelInfo3.deviceSerialNumber = 527115
        channelInfo3.hubPort            = 3
        channelInfo3.isHubPortDevice    = True
        channelInfo3.channel            = 0
        channelInfo3.isVINT             = False
        channelInfo3.netInfo.isRemote   = False

        ch3.setDeviceSerialNumber(channelInfo3.deviceSerialNumber)
        ch3.setHubPort(channelInfo3.hubPort)
        ch3.setIsHubPortDevice(channelInfo3.isHubPortDevice)
        ch3.setChannel(channelInfo3.channel)


        #setting DO 082818
        channelInfo4 = ChannelInfo()
        channelInfo4.deviceSerialNumber = 527115
        channelInfo4.hubPort            = 4
        channelInfo4.isHubPortDevice    = False
        channelInfo4.channel            = 0
        channelInfo4.isVINT             = False
        channelInfo4.netInfo.isRemote   = False

        ch4.setDeviceSerialNumber(channelInfo4.deviceSerialNumber)
        ch4.setHubPort(channelInfo4.hubPort)
        ch4.setIsHubPortDevice(channelInfo4.isHubPortDevice)
        ch4.setChannel(channelInfo4.channel)


        # setting motor 091118
        channelInfo5 = ChannelInfo()
        channelInfo5.deviceSerialNumber = 527115
        channelInfo5.hubPort            = 1
        channelInfo5.isHubPortDevice    = False
        channelInfo5.channel            = 0
        channelInfo5.isVINT             = True
        channelInfo5.netInfo.isRemote   = False

        ch5.setDeviceSerialNumber(channelInfo5.deviceSerialNumber)
        ch5.setHubPort(channelInfo5.hubPort)
        ch5.setIsHubPortDevice(channelInfo5.isHubPortDevice)
        ch5.setChannel(channelInfo5.channel)

        channelInfo6 = ChannelInfo()
        channelInfo6.deviceSerialNumber = 527115
        channelInfo6.hubPort            = 5
        channelInfo6.isHubPortDevice    = False
        channelInfo6.channel            = 0
        channelInfo6.isVINT             = True
        channelInfo6.netInfo.isRemote   = False

        ch6.setDeviceSerialNumber(channelInfo6.deviceSerialNumber)
        ch6.setHubPort(channelInfo6.hubPort)
        ch6.setIsHubPortDevice(channelInfo6.isHubPortDevice)
        ch6.setChannel(channelInfo6.channel)


        #setting release button 091918
        channelInfo7 = ChannelInfo()
        channelInfo7.deviceSerialNumber = 527122
        channelInfo7.hubPort            = 0
        channelInfo7.isHubPortDevice    = True
        channelInfo7.channel            = 0
        channelInfo7.isVINT             = False
        channelInfo7.netInfo.isRemote   = False

        ch7.setDeviceSerialNumber(channelInfo7.deviceSerialNumber)
        ch7.setHubPort(channelInfo7.hubPort)
        ch7.setIsHubPortDevice(channelInfo7.isHubPortDevice)
        ch7.setChannel(channelInfo7.channel)

        
        """
        * Add ch1 handlers before calling open so thch5.setCurrentLimitat no events are missed.
        """
        print("\n--------------------------------------")
        print("\nSetting OnAttachHandler...")
        ch.setOnAttachHandler(onAttachHandler)
        
        print("Setting OnDetachHandler...")
        ch.setOnDetachHandler(onDetachHandler)

        PrintEventDescriptions()


        """
        * Add ch2 & 3 handlers before calling open so that no events are missed.
        """
        print("\n--------------------------------------")
        print("\nSetting OnAttachHandler...")
        ch2.setOnAttachHandler(onAttachHandlerDI)
        
        print("Setting OnDetachHandler...")
        ch2.setOnDetachHandler(onDetachHandler)
        
       
        print("\n--------------------------------------")
        print("\nSetting OnAttachHandler...")
        ch3.setOnAttachHandler(onAttachHandlerDI)
        
        print("Setting OnDetachHandler...")
        ch3.setOnDetachHandler(onDetachHandler)

        print("\n--------------------------------------")
        print("\nSetting OnAttachHandler...")
        ch7.setOnAttachHandler(onAttachHandlerDI)
        
        print("Setting OnDetachHandler...")
        ch7.setOnDetachHandler(onDetachHandler)
     
        # this part is useful to send command after change in state
        #print("Setting OnStateChangeHandler...")
        #ch2.setOnStateChangeHandler(onStateChangeHandler)


        """
        * Add ch4 handlers before calling open so that no events are missed.
        """
        print("\n--------------------------------------")
        print("\nSetting OnAttachHandler...")
        ch4.setOnAttachHandler(onAttachHandlerDI)
        
        print("Setting OnDetachHandler...")
        ch4.setOnDetachHandler(onDetachHandler)
        
       

        """
        * Add Ch 5 6 event handlers before calling open so that no events are missed.
        """
        print("\n--------------------------------------")
        print("\nSetting OnAttachHandler...")
        ch5.setOnAttachHandler(onAttachHandlerStepper)
        ch6.setOnAttachHandler(onAttachHandlerStepper)

       
        """
        * setting text file and camera
        """

        f = open("data\data.txt","a")
        cap = cv2.VideoCapture(0)
        ret = cap.set(3,320)
        ret = cap.set(4,240)

        """
        * Open the channel with a timeout
        """
 
        print("\nOpening and Waiting for Attachment...")
        
        try:
            ch.openWaitForAttachment(5000)
            ch2.openWaitForAttachment(5000)
            ch3.openWaitForAttachment(5000)
            ch4.openWaitForAttachment(5000)
            ch5.openWaitForAttachment(5000)
            ch6.openWaitForAttachment(5000)
            ch7.openWaitForAttachment(5000)
        except PhidgetException as e:
            PrintOpenErrorMessage(e, ch)
            raise EndProgramSignal("Program Terminated: Open Failed")
        
 
        gain = ch.getBridgeGain()
        print("gain = " + str(gain))

        ch4DO = 0;
        ch4.setDutyCycle(ch4DO)

        #091118 set parameters of stepper
        ch5.setAcceleration(100000)
        ch6.setAcceleration(100000)
        Acc = ch5.getAcceleration()
        print(Acc)

        ch5.setCurrentLimit(0.5)
        ch6.setCurrentLimit(0.5)
        Cl = ch5.getCurrentLimit()
        print(Cl)

        ch5.setVelocityLimit(20000)
        ch6.setVelocityLimit(20000)
        Vel = ch5.getVelocityLimit()
        print(Vel)

        ch5.setHoldingCurrentLimit(0.5)
        ch6.setHoldingCurrentLimit(0.5)

         ## Try to record gradual latching data
        MouseName = input("Please type the mouse name :  ")
        Latching = [30,30,45,45,60,60,80,100,120,150,180,240,300,360,420,480,600,600,900,900,1200,1200,1200,1800]
        Name = MouseName +'.txt'
        path = 'C:/Users/labadmin/Documents/Python/Latching/{0}/'.format(MouseName)

        try:
            latching_file = open(path+Name,'r')                                                                                                   
            listLatching = latching_file.readlines()
            latching_file.close()
            latching_times = []

            for x in listLatching:
                latching_times.append(x.split(' ')[0])
                index1 = latching_times[-1]
                
            index = float(index1) +1
            
            try:                
                duration = Latching[index]
            except:
                duration = 1800
            
        except:
            os.makedirs('C:/Users/labadmin/Documents/Python/Latching/{0}/'.format(MouseName)) # if it's the mouse 1st day of latching, then create the folder
            index = 0
            duration = Latching[index]
            latch = 1
            bad_perf = 0
            f1 = open(path+Name,"a+") # create the new text file
            f1.write('%d' % index + ' %d' % duration + ' %d' % latch + ' %d ' % bad_perf)
            f1.close()

        ################################################################
        Pos = 0

        # execute the main loop
        x = 0
        
        starttime = time.time()
        try:
            while True:
                x = x+1
                
                #time.sleep(0.1)
                time.sleep(0.1 - (time.time()-starttime)%0.1)

                if 'vol' in locals():
                    volBefore = vol
                else:
                    volBefore = 0
                    
                vol = ch.getVoltageRatio()
                vollist = abs(vol - volBefore) * 1000
                ch2Stat = ch2.getState()
                ch3Stat = ch3.getState()
                ch7Stat = ch7.getState()
                timeInS = time.perf_counter()
                now=datetime.now()         
                f.write(str(timeInS)+"   "+str(vol)+"  "+str(ch2Stat)+" "+str(ch3Stat)+" "+str(Pos)+" "+str(now)+"\n")

                # if front panel sensor is on, set Ch4 DO on
                if ch2Stat + ch3Stat < 2:
                    if  ch4DO == 0:
                        ch4DO = 1;
                    else:
                        ch4DO = 0
 
                else:
                    ch4DO = 0
                    #print('DO off')

                
                # read text files
                latching_file = open(path+Name,'r')                                                                                                   
                listLatching = latching_file.readlines()
                latching_file.close()
                latching_times = []

                for z in listLatching:
                    latching_times.append(z.split(' ')[0])
                    index1 = latching_times[-1]
                
                index = int(index1)

                try:
                    release_time = time.perf_counter() - stop
                except:
                    stop = 0
                    release_time = time.perf_counter() - stop
                    
                # auto latching if both sides of the head bar are on
                if ch2Stat + ch3Stat <= 1 and release_time > 10:    # don't start another latching within 10 sec, give mice time to leave               
                    if Pos == 0:
                        if ch5.getIsMoving() + ch6.getIsMoving() == 0:
                            ch5.setTargetPosition(-1300)
                            ch6.setTargetPosition(1600)
                            Pos = -1000
                            print('Pos on')
                            start = time.perf_counter()
                            #f1.write(' \n%d' % index + ' %d' % duration )
                            if index < 24:                                
                                duration = Latching[index]
                            else:
                                duration = 1800         
                            
                                                    

                ch4.setDutyCycle(ch4DO)
                bad_perf = 0
                # every 10 cycle ie 1s save images
                if x%10==0:
                    # Capture frame-by-frame    
                    ret, frame = cap.read()
                    
                    # Display the resulting frame
                    #cv2.imshow('image',frame) # it is too fast to do this
                    cv2.imwrite('data\images{0}.jpg'.format(math.floor(x/10)),frame)

                    # print the Vol
                    print('vol = ' + str(vol) +', ch2 state =' + str(ch2Stat) +', ch3 state =' + str(ch3Stat))
                    print(str(vollist))
                    if 'start' in locals():
                        print(str(start) + '  '+str((time.clock() - start)))

                    # read the last line to check performance from Bpod (matlab)
                    bad_perf = 0
                    if Pos == -1000:
                        f1 = open(path+Name,"r")
                        latching_info = f1.readlines()                        
                        bad_perf1 = []
                        try:
                            print('good')
                            for y in latching_info: # load recent x, y, z location: last line
                                    bad_perf1.append(y.split(' ')[3])                                    
                                    bad_perf = bad_perf1[-1]  # first column in the last line                                    
                        except:
                            #bad_perf = 0
                            print('bad')
                        f1.close()
                            
                bad_perf = int(bad_perf)  

                # autorelease by load cell threshold 12242018
                if Pos == -1000:
                    if bad_perf == 1:
                        ch5.setTargetPosition(0)
                        ch6.setTargetPosition(0)
                        Pos = 0
                        del start                        
                        print('Pos off')
                        stop = time.clock()
                        latch = 0
                        bad_perf = 0
                        with open(path+Name,"a") as f1:
                            f1.write(' \n%d' % index + ' %d' % duration + ' %d' % latch + ' %d ' % bad_perf)
                        index = index
                    elif vollist > 0.30 and time.clock() - start >10:
    ##                    if vol > 0.0011:
                        ch5.setTargetPosition(0)
                        ch6.setTargetPosition(0)
                        Pos = 0
                        del start                        
                        print('Pos off')
                        stop = time.clock()
                        latch = 0
                        with open(path+Name,"a") as f1:
                            f1.write(' \n%d' % index + ' %d' % duration + ' %d' % latch + ' %d ' % bad_perf )
                        index = index
                    elif vollist > 0.26 and time.clock() - start > 10:
                        ch5.setTargetPosition(0)
                        ch6.setTargetPosition(0)
                        Pos = 0
                        del start                        
                        print('Pos off')
                        stop = time.clock()
                        latch = 0
                        with open(path+Name,"a") as f1:
                            f1.write(' \n%d' % index + ' %d' % duration + ' %d' % latch + ' %d ' % bad_perf)
                        index = index
                    elif time.clock() - start > duration: # 6 min
                        ch5.setTargetPosition(0)
                        ch6.setTargetPosition(0)
                        Pos = 0
                        del start
                        stop = time.clock()
                        print('Pos off')
                        latch = 1
                        index = index +1
                        with open(path+Name,"a") as f1:
                            f1.write(' \n%d' % index + ' %d' % duration + ' %d' % latch + ' %d ' % bad_perf)
                                      

            
                # toggle head bar
                # if the switch is on and motor is not moving
                if ch7Stat == 1:
                    if ch5.getIsMoving() + ch6.getIsMoving() == 0:

                        if Pos == 0:
                            ch5.setTargetPosition(-1300)
                            ch6.setTargetPosition(1300)
                            Pos = -1000
                            print('Pos on') 
                        
                        elif Pos == -1000:
                            ch5.setTargetPosition(0)
                            ch6.setTargetPosition(0)
                            Pos = 0
                            if 'start' in locals():
                                del start                            
                            print('Pos off')

                    
        except KeyboardInterrupt:
            pass # Ctrl+C to stop

        
        
        """
        * Perform clean up and exit
        """

        #clear the VoltageRatioChange event handler 
        ch.setOnVoltageRatioChangeHandler(None)  
        #clear the SensorChange event handler
        ch.setOnSensorChangeHandler(None)
        ch2.setOnStateChangeHandler(None)
        
        print("\nDone Sampling...")

        print("Cleaning up...")
        ch.close()
        f.close()
        f1.close
        print("\nExiting...")        
        

        return 0

    except PhidgetException as e:
        sys.stderr.write("\nExiting with error(s)...")
        DisplayError(e)
        traceback.print_exc()
        print("Cleaning up...")
        ch.setOnVoltageRatioChangeHandler(None)
        ch.setOnSensorChangeHandler(None)
        ch.close()
        return 1
    except EndProgramSignal as e:
        print(e)
        print("Cleaning up...")
        ch.setOnVoltageRatioChangeHandler(None)
        ch.setOnSensorChangeHandler(None)
        ch.close()
        return 1
    finally:
        print("Press ENTER to end program.")
        readin = sys.stdin.readline()

main()

