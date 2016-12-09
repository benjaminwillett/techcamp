from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle,Color
from kivy.uix.button import Button
from kivy.properties import NumericProperty, StringProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.core.window import Window
import time
import random

class TargetChar(Label):
    char=StringProperty("f")
    location=NumericProperty(200)
    
class TouchTyperGUI(Widget):
    Percentage = NumericProperty(0)
    Speed = NumericProperty(0)
    KeyCount=0
    CorrectCount=0
    StartTime=time.time()
    tc1 = ObjectProperty(None)
    chars="fjdksla;ghvnrueiwoqpcm,x.z/"
    def __init__(self):
        super(TouchTyperGUI, self).__init__()
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
    def update (self,dt):
        self.tc1.location+=10
        if self.tc1.location>self.height :
            self.tc1.location=30
        if self.KeyCount!=0:
            self.Percentage=round(100*float(self.CorrectCount)/float(self.KeyCount),1)
        self.Speed=round(12*float(self.KeyCount)/(time.time()-self.StartTime),1)
        pass
    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def new_key(self):
        self.tc1.location=60
        charno=random.randint(0,len(self.chars)-1)
#        self.tc1.char="h"
#        print(self.chars[charno:charno+1])
        self.tc1.char=self.chars[charno:charno+1]
    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        keyhit=keycode[1]
        self.KeyCount+=1
        if keyhit==self.tc1.char:
            self.CorrectCount+=1
        self.new_key()
        return True
class TouchTyperApp(App):
    def build(self):
        print("getting GUI")
        GUI = TouchTyperGUI()
        Clock.schedule_interval(GUI.update, 0.2)
        print("returning")
        return GUI

if __name__ == '__main__':
    print("setting up touch typing app")
    TouchTyperApp().run()
    print("TyperApp complete")

    
    
    
# to be completed by