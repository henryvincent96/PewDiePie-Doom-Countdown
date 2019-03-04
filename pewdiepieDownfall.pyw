import urllib.request
import json
import time
import platform
import threading
import os
from appJar import gui

#gets sub count from youtube for a given channel ID
def getSubCount(id):
    data = urllib.request.urlopen('https://www.googleapis.com/youtube/v3/channels?part=statistics&id=' 
    + id + '&key=' + key).read()
    return json.loads(data.decode('utf-8'))['items'][0]['statistics']['subscriberCount']

#Calculates the difference between PewDiePie and T Series
#For optimisation, sub counts are global variables
def getCountdown():
    global pdpCount, tseriesCount
    pdpCount = int(getSubCount(pdpID))
    tseriesCount = int(getSubCount(tseriesID))
    return pdpCount - tseriesCount

#variables required for API
key = 'AIzaSyBR7ZQmh02ETze1hjNS7rFYsSJSBYoUsvY'
pdpID = 'UC-lHJZR3Gqxm24_Vd_AJ5Yw'
tseriesID = 'UCq-Fj5jknLsUf-MWSy4_brA'

exitFlag = False

class Counter (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        print('Starting ' + self.name)
        startCounter(self.name, 5, self.counter)
        print('Exiting ' + self.name)

#init
pdpCount = 0
tseriesCount = 0
netChange = 0
previousCount = 0
newCount = getCountdown()
connectionFault = False
connectionFaultState = False

def startCounter(threadName, counter, delay):
    global newCount, netChange, connectionFault
    while True:
        #logic
        try:
            if(exitFlag):
                threadName.exit()

            previousCount = newCount
            newCount = abs(getCountdown())
            netChange = newCount - previousCount

            if netChange >= 0:
                netChange = str('+' + str(netChange))

            if (connectionFault): connectionFault = False
        except TimeoutError:
            print('Timeout error')
            connectionFault = True
        except urllib.error.URLError:
            print('URL error')
            connectionFault = True
        #don't really want google thinking I'm DDOSing them
        time.sleep(delay)

counterThread = Counter(1, "Counter", 1)
counterThread.start()

#GUI labels
pSubCountTtl = 'pSubCountTtl'
pSubCountVal = 'pSubCountval'
tSubCountTtl = 'tSubCountTtl'
tSubCountVal = 'tSubCountVal'
diffTtl = 'diffTtl'
diffVal = 'diffVal'
netChangeVal = 'netChangeVal'
errorTtl = 'errorTtl'

#Setup GUI
app = gui('PewDiePie Doom Countdown', showIcon=False)
app.setSize(330, 153)
app.setResizable(True)
app.setBg('white', True, False)
app.setStretch("column")
app.setSticky("nesw")
app.setPadding([5,0])

#Create labels
app.addLabel(pSubCountTtl, 'PewDiePie', 0, 0)
app.addLabel(tSubCountTtl, 'TSeries', 0, 1)
app.addLabel(diffTtl, 'Difference', 2, 0, colspan=2)
app.addLabel(errorTtl, '', 5, 0)

app.addLabel(pSubCountVal, '{:,}'.format(pdpCount), 1, 0)
app.addLabel(tSubCountVal, '{:,}'.format(tseriesCount), 1 ,1)
app.addLabel(diffVal, '{:,}'.format(newCount), 3, 0, colspan=2)
app.addLabel(netChangeVal, str(netChange), 4, 0, colspan=2)

#Configure label style
globalFont = 'Helvetica'
wTitle = globalFont + ' 8 bold'
wTitleColour = '#828282'
channelValue = globalFont + ' 14'

app.getLabelWidget(pSubCountTtl).config(font=wTitle)
app.setLabelFg(pSubCountTtl, wTitleColour)
app.getLabelWidget(tSubCountTtl).config(font=wTitle)
app.setLabelFg(tSubCountTtl, wTitleColour)
app.getLabelWidget(diffTtl).config(font=wTitle)
app.setLabelFg(diffTtl, wTitleColour)

app.getLabelWidget(pSubCountVal).config(font=channelValue)
app.getLabelWidget(tSubCountVal).config(font=channelValue)

app.getLabelWidget(diffVal).config(font=globalFont + ' 20')
app.getLabelWidget(netChangeVal).config(font=globalFont + ' 11')
app.setLabelFg(netChangeVal, wTitleColour)

#update labels
def updateValLabels():
    global connectionFault, connectionFaultState
    
    if(connectionFaultState != connectionFault):
        connectionFaultState = connectionFault
        if(connectionFault):
            app.setLabel(errorTtl, 'CONNECTION FAULT')
        else:
            app.setLabel(errorTtl, '')
    elif(not(connectionFault)):
        app.setLabel(pSubCountVal, '{:,}'.format(pdpCount))
        app.setLabel(tSubCountVal, '{:,}'.format(tseriesCount))
        app.setLabel(diffVal, '{:,}'.format(newCount))
        app.setLabel(netChangeVal, str(netChange))

def quitBehaviour():
    os._exit(0)

app.registerEvent(updateValLabels)
app.setStopFunction(quitBehaviour)

#LaunchGUI
app.go()