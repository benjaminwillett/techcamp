import serial
import serial.tools.list_ports as SerialListPorts
import sys
import traceback
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle,Color
from kivy.uix.button import Button
from kivy.properties import NumericProperty, StringProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.uix.image import Image

class robot (object):
    RetryCount=0
    BatteryVoltage=0.0
    ''' provide container for connection to bluetooth connected robot'''
    def __init__(self):
        '''Searches comm ports on computer and connects to first bluetooth serial port '''
        #self.ser=serial.Serial('COM20', 115200)
        self.Connect()
            
    def __del__(self):
        '''closes com port connection'''
        self.ser.close()
    def Connect(self):
        #print("connecting")
        SerialList=list(SerialListPorts.comports())
        myPort=""
        for Port in SerialList:
            if "Bluetooth" in Port[1]:
                myPort=Port[0]
        if myPort!="":
            try:
                #print("connecting")
                self.ser=serial.Serial(myPort, 115200,timeout=1)
                #print("setting timeout")
                self.ser.setWriteTimeout(1)
            except serial.SerialTimeoutException:
                print ("Lost Contact with Robot")
                self.ser=None
            except serial.SerialException:
                print("No contacted with Robot")
                self.ser=None
        else:
            print("No port found")
            self.ser=None
    def SendSignal(self,msg):
        ret_value=""
        #print("In Send Signal " + msg)
        if self.ser is None:
            #print("try connected")
            self.Connect()
        if self.ser==None:
            print("No Robot Connected")
            if ret_value=="":
                ret_value="Not Connected\n"
        else:
            try:
                self.ser.write(msg)
                #print("Sent Message")
                ret_value=self.ser.readline()
                #print("received message")
                if ret_value!="":
                    self.RetryCount=0
                else:
                    #print("Retry Count " + str(self.RetryCount))
                    self.RetryCount+=1
            except serial.SerialTimeoutException:
                print ("Lost Contact with Robot")
                if ret_value=="":
                    self.RetryCount+=1
                    ret_value="Failed\n"
            except serial.serialutil.SerialTimeoutException:
                print ("Lost Contact with Robot")
                if ret_value=="":
                    self.RetryCount+=1
                    ret_value="Failed\n"
            except AttributeError:
                print("attribute error")
                if self.ser==None:
                    print("No Robot Connected")
                    if ret_value=="":
                        ret_value="Not Connected\n"
                else:
                    print ("Unexpected error:", sys.exc_info()[0])
                    traceback.print_exc()
                    self.RetryCount+=1
                    ret_value="Failed\n"
            except ValueError:
                print ("Unexpected error:", sys.exc_info()[0])
                traceback.print_exc()
                pass
                    
            if self.RetryCount >5 :
                print("resetting serial port")
                self.ser=None
            #print ("Signal " + msg + " Resulted in result of " + ret_value)
        return ret_value
    
    def forward(self,steps=4):
        '''increase power in both left and right motors by 40 '''
        ret_value=self.SendSignal("f")
        return ret_value
    def right(self,steps=4):
        ''' increases left motor by 40 and decreases right motor by 40'''
        ret_value=self.SendSignal("r")
        return ret_value
    def left(self,steps=4):
        ''' increases right motor by 40 and decreases left motor by 40'''
        for i in range(0,steps):
            ret_value=self.SendSignal("l")
        return ret_value
    def back(self,steps=4):
        ''' decrases power on both left and right motor by 40'''
        for i in range(0,steps):
            ret_value=self.SendSignal("b")

        return ret_value
    def stop(self):
        '''Sets power to both he left and right motors to 0'''
        ret_value=self.SendSignal("s")
        return ret_value
    def distance(self):
        ''' This returns the distance to objects from the robot
        Three values are returned, which represent distance in cm 
        angle of these readings are -15deg 0deg and 15deg'''
        ret_value=self.SendSignal("d")
        return ret_value
    def power(self):
        '''provide current power on driving motor'''
        ret_value=self.SendSignal("p")
        return ret_value
    def compass(self):
        '''provides compass bearings of robot'''
        ret_value=self.SendSignal("c")
        return ret_value
    def battery(self):
        retval=self.SendSignal("v")
        return retval
class PowerBars(Widget):
    Power = NumericProperty(50)
class BatteryImage(Image):
    source=StringProperty("Battery6.png")
class BluetoothImage(Image):
    source=StringProperty("NoBluetooth.png")
class CompassImage(Image):
    angle=NumericProperty(0)
class ControllerGUI(Widget):
    UpdateIndex=0
    LeftDistance = NumericProperty(0)
    ForwardDistance = NumericProperty(0)
    RightDistance = NumericProperty(0)
    Bearing=NumericProperty(0)
    plu = ObjectProperty(None)
    pru = ObjectProperty(None)
    pll = ObjectProperty(None)
    prl = ObjectProperty(None)
    compass= ObjectProperty(None)
    batimage =ObjectProperty(None)
    Battery=0.0
    
    def __init__(self):
        super(ControllerGUI, self).__init__()
        print("in __init__")
        self.MyRobot=robot()
        self.UpdatePower(0,0)
    def update(self,dt):
        #print("update " + str(self.UpdateIndex))
        #Go through a couple of states to spread out the update
        if self.UpdateIndex==0:
            #Get compass angle
            self.updateCompass()
        elif self.UpdateIndex==1:
            #update distance sensors
            try:
                distance=self.MyRobot.distance()[2:]  #get rid of the D:
                if distance not in ["Failed\n","Not Connected\n"]: 
                    self.LeftDistance=float(distance[:distance.find(",")])
                    distance=distance[distance.find(",")+1:]
                    self.ForwardDistance=float(distance[:distance.find(",")])
                    distance=distance[distance.find(",")+1:]
                    self.RightDistance=float(distance)
                else:
                    self.ForwardDistance=0.0
                    self.LeftDistance=0.0
                    self.RightDistance=0.0

            except:
                self.ForwardDistance=0.0
                self.LeftDistance=0.0
                self.RightDistance=0.0
            #print(self.MyRobot.distance())
        elif self.UpdateIndex==2:
         #update power
         #   print(self.MyRobot.power())
            self.DecodeReply(self.MyRobot.power())
        elif self.UpdateIndex==3:
            self.UpdateBattery()
        elif self.UpdateIndex>=4:
            self.UpdateIndex=-1
        #print("in update")
        self.UpdateBluetooth()
        self.UpdateIndex+=1
    def StopButton(self):
        #print("Stop button pressed")
        self.MyRobot.stop()
    def ForwardButton(self):
        #print("Forward button pressed")
        self.DecodeReply(self.MyRobot.forward(1))
        #print("Forward: " + str(left) + " Right: " + str(right))
    def BackwardButton(self):
        #print("Backward button pressed")
        self.DecodeReply(self.MyRobot.back(1))
    def LeftButton(self):
        #print("Left button pressed")
        self.DecodeReply(self.MyRobot.left(1))
    def RightButton(self):
        #print("Right button pressed")
        self.DecodeReply(self.MyRobot.right(1))
    def DecodeReply(self,msg):
        left=0
        right=0
        try:
            if (msg.find(":")>0) :
                left=int(msg[msg.find(":")+1:msg.find(",")])
            else:
                left=int(msg[msg.find(" "):msg.find(",")])
            #print("left:" + str(left))
            
            right=int(msg[msg.find(",")+1:])
            self.UpdatePower(left,right)
        except:
            print("failed to convert " + msg)
            # print("start" + str(msg.find(":")+1))
        return [left,right]
    def UpdatePower(self,left=0,right=0):
        self.pll.Power=0
        self.prl.Power=100
        self.pru.Power=0
        if (left >0):
            self.plu.Power=left
            self.pll.Power=0
        else:
            self.plu.Power=0
            self.pll.Power=-left
        if (right >0):
            self.pru.Power=right
            self.prl.Power=0
        else:
            self.pru.Power=0
            self.prl.Power=-right
    def updateCompass(self):
        try:
            self.b0.size_element=50
            RobotReply=self.MyRobot.compass()
            if RobotReply not in ["Failed\n","Not Connected\n"]: 
                self.Bearing=float(RobotReply[2:])
                self.compass.angle=float(RobotReply[2:])
            else:
                self.Bearing=0.0
        except:
            self.Bearing=0.0
            #print(self.MyRobot.compass())
    def UpdateBattery(self):
        try:
            RobotReply=self.MyRobot.battery()
            if RobotReply not in ["Failed\n","Not Connected\n"]: 
                #print("about to test")
                if self.Battery==0.0:
                    #print("ok it was zero")
                    self.Battery=float(RobotReply[2:])
                else:
                    #print("it was not zeor")
                    self.Battery=0.1*float(RobotReply[2:])+0.9*self.Battery
                #self.Battery.power=float(RobotReply[2:])
            else:
                self.Battery=0.9*self.Battery
        except:
            self.Battery=0.0
            print("Updatebattery call had an error")
            #print(self.MyRobot.compass())
        batteryimageno=str(max(min(int((self.Battery-3.8)*7.0/1.2),7),0))
        self.batimage.source="battery" + batteryimageno + ".png"
        print("battery returned " + batteryimageno)
    def UpdateBluetooth(self):
        if self.MyRobot.ser!=None:
            self.blueimage.source="bluetooth.png"
        else:
            self.blueimage.source="NoBluetooth.png"
        
        pass
class ControllerApp(App):
    def build(self):
        print("getting GUI")
        GUI = ControllerGUI()
        Clock.schedule_interval(GUI.update, 1.0)
        print("returning")
        return GUI
    def StopButton(self):
        print("ControllerApp stop pressed")
class PowerBar(Widget):
    Power = NumericProperty(50)
    
         
if __name__ == '__main__':
    print("setting up controller app")
    ControllerApp().run()
    print("Controller App complete")
        