import kivy
import numpy as np
import tensorflow as tf
import os
import sys
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock, mainthread
from tensorflow.keras.layers import *
from jnius import autoclass, cast

if "posix" == os.name and "ANDROID_ROOT" in os.environ:
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
    Context = cast('android.content.Context', PythonActivity.getApplicationContext)
kivy.require('1.10.1')
apppath = '/home/eomsehwan/MachineLearning/369app'
kivy.Config.set('kivy', 'default_font', ["NanumBarunGothic", apppath+"/nanum/NanumBarunGothic.ttf"])
num_digits = 10
epoch = 300
batch = 300
l=4
checkpt = apppath+'/model/369_{}d_{}e_{}b.h5'.format(num_digits,epoch,batch)
checkpt2 = apppath+'./model/369_{}d_{}e_400b-2.h5'.format(num_digits,epoch)
checkpoint_path = apppath+'/model/369_{}d_{}e_{}b/cp.ckpt'.format(num_digits, epoch, batch)
n = 1
tsn0 = ""
result = ""
ai1 = "AI1 : "
ai2 = "\nAI2 : "
ai3 = "\nAI3 : "
reason = ""
tsnlist = ["플레이어 : "]
btn = '게임 시작!'

def tsn_encode(i):
	I0 = str(i)
	y = 0
	for I in I0:
		if I in "369":
			y += 1
	return np.array([1 if j == y else 0 for j in range(l)])

def tsn(i):
    List = [str(i)] + ['x'*i for i in range(1, l)]
    return List[np.argmax(tsn_encode(i))]

def tsn_decode(i, prediction):
    List = [str(i)] + ['x'*i for i in range(1, l)]
    return List[prediction]

def binary_encode(i):
    i = list(map(str, list(i)))
    i = [list("0" * (l - len(j)) * (len(j) < l) + j) for j in i]
    i = np.array([np.array(list(map(ord, j))) for j in i])
    i = np.array([[[k >> d & 1 for d in range(7)] for k in j] for j in i])
    return i

model = tf.keras.models.load_model(checkpt)

num_hidden1 = 400
num_hidden2 = 800
num_hidden3 = 1200
num_hidden4 = 1600
num_hidden5 = 2000
num_hidden6 = 2000

model2 = tf.keras.models.Sequential([
    Flatten(input_shape = (4, 7)),
    Dense(num_hidden1, activation="relu"),
    Dropout(0.5),
    Dense(num_hidden2, activation="relu"),
    Dropout(0.4),
    Dense(num_hidden3, activation="relu"),
    Dropout(0.3),
    Dense(num_hidden4, activation="relu"),
    Dropout(0.2),
    Dense(num_hidden5, activation="relu"),
    Dropout(0.1),
    Dense(num_hidden6, activation="relu"),
    Dense(l, activation="softmax")
])
model2.load_weights(checkpoint_path)

model3 = tf.keras.models.Sequential([
    Flatten(input_shape = (4, 7)),
    Dense(num_hidden2, activation="relu"),
    Dropout(0.5),
    Dense(num_hidden4, activation="relu"),
    Dropout(0.4),
    Dense(num_hidden6, activation="relu"),
    Dense(l, activation="softmax")
])
model3.load_weights(checkpt2)

class StartScreen(Screen):
    name = StringProperty('Start')

class PlayMenuScreen(Screen):
    name = StringProperty('Playmenu')

class PlayScreen(Screen):
    name = StringProperty('Play')

class BenchScreen(Screen):
    name = StringProperty('Bench')

class LoseScreen(Screen):
    name = StringProperty('Lose')

class WinScreen(Screen):
    name = StringProperty('Win')

class Upper_bar(BoxLayout):
    pass

class Lower_bar(BoxLayout):
    pass

class RootWidget(Widget):
    import time
    TSN = StringProperty(tsn0)
    NOW = 0
    n = 1
    n0 = StringProperty(str(n))
    difficulty = 0
    now = 0
    now0 = StringProperty(str(now))
    deltatime = 0
    deltat = StringProperty(str(deltatime))
    delta = StringProperty("")
    turn = 0
    Turn = StringProperty(str(turn))
    screen_manager = ObjectProperty(None)
    start1 = 1
    start2 = 1
    start3 = 1
    l1 = 1
    l2 = 1
    l3 = 1
    str1 = StringProperty(ai1)
    str2 = StringProperty(ai2)
    str3 = StringProperty(ai3)
    Reason = StringProperty(reason)
    startbtn = StringProperty(btn)

    def __init__(self, *args, **kwargs):
        super(RootWidget, self).__init__(*args, **kwargs)

    def thread(self):
        Clock.schedule_interval(self.play, 0.00001)

    def thread2(self):
        Clock.schedule_interval(self.benchmark, 0.00001)

    def threadpause(self):
        Clock.unschedule(self.benchmark, 0.00001)

    def startpress(self):
        if self.startbtn == '게임 시작!':
            self.startbtn = '메인 화면으로'
            self.TSN += "플레이어 : "
            self.NOW = 1
            self.now = self.time.time()
            self.thread()
        elif self.startbtn == '메인 화면으로':
            Clock.unschedule(self.play, 0.00001)
            self.set_state('Start')
            self.startbtn = '게임 시작!'
            self.initialize()

    def initialize(self):
        global tsn0, tsnlist
        self.TSN = tsn0
        self.NOW = 0
        self.n = 1
        self.n0 = str(n)
        self.now = 0
        self.now0 = str(self.now)
        self.deltatime = 0
        self.deltat = str(self.deltatime)
        self.delta = str(self.deltatime)
        self.turn = 0
        self.Turn = str(self.turn)
        self.start1 = 1
        self.start2 = 1
        self.start3 = 1
        self.l1 = 1
        self.l2 = 1
        self.l3 = 1
        self.str1 = ai1
        self.str2 = ai2
        self.str3 = ai3
        self.Reason = reason
        tsnlist = ["플레이어 : "]
        startbtn = btn

    def on_state(self, instance, value):
        if value == 'Start':
            self.screen_manager.current = 'Start'

    def set_state(self, state):
        self.screen_manager.current = state

    def tsn_include(self, N):
        global result, tsnlist
        if self.NOW == 1:
            self.deltatime = self.time.time() - self.now
            self.deltat = str(self.deltatime)
            if N:
                result = "x" * N
            else:
                result = str(self.n)
            self.TSN += result + "\n"
            tsnlist.append(result+"\n")
            self.NOW = 0

    def play(self, dt):
        global result, tsnlist
        seconds = 9 - 2 * self.difficulty
        self.deltatime = self.time.time() - self.now
        self.deltat = str(self.deltatime)
        self.delta = str(seconds - self.deltatime)

        if self.turn == 0:
            self.now0 = str(self.now)
            if self.deltatime > seconds:
                self.Reason = "너무 늦었네요..."
                self.screen_manager.current = 'Lose'
                Clock.unschedule(self.play, 0.00001)
        elif self.turn == 1:
            x = binary_encode([self.n])
            Y = np.argmax(model.predict(np.array(x)), axis=1)
            result = tsn_decode(self.n, Y[0])
            self.TSN += "AI1 : " + result + "\n"
            tsnlist.append("AI1 : " + result + "\n")
        elif self.turn == 2:
            x = binary_encode([self.n])
            Y = np.argmax(model2.predict(np.array(x)), axis=1)
            result = tsn_decode(self.n, Y[0])
            self.TSN += "AI2 : " + result + "\n"
            tsnlist.append("AI2 : " + result + "\n")
        elif self.turn == 3:
            x = binary_encode([self.n])
            Y = np.argmax(model3.predict(np.array(x)), axis=1)
            result = tsn_decode(self.n, Y[0])
            self.TSN += "AI3 : " + result + "\n"
            tsnlist.append("AI3 : " + result + "\n")

        if self.NOW == 0:
            if result != tsn(self.n) and self.turn == 0:
                self.Reason = "틀리셨네요..."
                self.screen_manager.current = 'Lose'
                Clock.unschedule(self.play, 0.00001)
            elif result != tsn(self.n) and self.turn != 0:
                self.screen_manager.current = 'Win'
                Clock.unschedule(self.play, 0.00001)
            self.n += 1
            self.n0 = str(self.n)
            self.turn += 1
            self.Turn = str(self.turn)
            
            if self.turn > 3:
                self.turn = 0
                self.Turn = str(self.turn)
                self.NOW = 1
                self.TSN += "플레이어 : "
                tsnlist.append("플레이어 : ")
                self.now = self.time.time()
                if len(tsnlist) >= 45:
                	tsnlist = tsnlist[5:49]
                	self.TSN = "".join(tsnlist)

    def benchmark(self, dt):
        if self.l1:
            x = binary_encode([self.start1])
            Y = np.argmax(model.predict(np.array(x)), axis=1)
            ans = tsn_decode(self.start1, Y[0])
            if ans != tsn(self.start1):
                self.l1 = 0
            self.start1 += 1
        if self.l2:
            x = binary_encode([self.start2])
            Y = np.argmax(model2.predict(np.array(x)), axis=1)
            ans = tsn_decode(self.start2, Y[0])
            if ans != tsn(self.start2):
                self.l2 = 0
            self.start2 += 1
        if self.l3:
            x = binary_encode([self.start3])
            Y = np.argmax(model3.predict(np.array(x)), axis=1)
            ans = tsn_decode(self.start3, Y[0])
            if ans != tsn(self.start3):
                self.l3 = 0
            self.start3 += 1
            
        if self.l1+self.l2+self.l3 == 0:
            Clock.unschedule(self.benchmark, 0.00001)
        else:
            self.str1 = ai1 + str(self.start1-1)
            self.str2 = ai2 + str(self.start2-1)
            self.str3 = ai3 + str(self.start3)
            
    def finish(self):
        sys.exit()

class AI369App(App):
    def build(self):
        return RootWidget()

if __name__ == '__main__':
    AI369App().run()
