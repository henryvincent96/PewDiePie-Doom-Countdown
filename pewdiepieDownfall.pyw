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
errorTtl = 'errorTtl'

#Setup GUI
app = gui('PewDiePie Doom Countdown', showIcon=False)
app.setResizable(canResize=True)
app.setSize(330, 86)
app.setFont(size=11)
app.setStretch("none")
app.setSticky("w")

app.addLabel(pSubCountTtl, 'PewDiePie Sub Count:', 0, 0)
app.addLabel(tSubCountTtl, 'TSeries Sub Count:', 1, 0)
app.addLabel(diffTtl, 'Current Difference:', 2, 0)
app.addLabel(errorTtl, '', 3, 0)

app.addLabel(pSubCountVal, '{:,}'.format(pdpCount), 0, 1)
app.addLabel(tSubCountVal, '{:,}'.format(tseriesCount), 1 ,1)
app.addLabel(diffVal, '{:,}'.format(newCount) + ' (' + str(netChange) + ')', 2, 1)

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
        app.setLabel(diffVal, '{:,}'.format(newCount) + ' (' + str(netChange) + ')')

def quitBehaviour():
    os._exit(0)

app.registerEvent(updateValLabels)
app.setStopFunction(quitBehaviour)

#LaunchGUI
app.go()