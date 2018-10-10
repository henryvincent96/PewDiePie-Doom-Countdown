import urllib.request
import json
import time
import platform
import threading
from os import system
from appJar import gui

def setClearScreenCommand():
    thisPlatform = platform.system()
    if (thisPlatform == 'Windows'):
        return 'cls'
    elif (thisPlatform == 'Linux'):
        return 'clear'

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
#Yes, I know my API key is public, but I'm hoping people won't abuse that. API keys are free you know.
key = 'AIzaSyBR7ZQmh02ETze1hjNS7rFYsSJSBYoUsvY'
pdpID = 'UC-lHJZR3Gqxm24_Vd_AJ5Yw'
tseriesID = 'UCq-Fj5jknLsUf-MWSy4_brA'

exitFlag = 0

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

def startCounter(threadName, counter, delay):
    global newCount
    while True:
        #logic
        try:
            if(exitFlag):
                threadName.exit()

            previousCount = newCount
            newCount = getCountdown()
            netChange = newCount - previousCount

            if netChange >= 0:
                netChange = str('+' + str(netChange))
        except TimeoutError:
            print('Timeout error')
        except urllib.error.URLError:
            print('URL error')
        #don't really want google thinking I'm DDOSing them
        time.sleep(delay)

counterThread = Counter(1, "CounterThread", 1)
counterThread.start()
print('Exiting main thread')

app = gui('PewDiePie Doom Countdown', '350X100')

app.addLabel('pSubCountTtl', 'PewDiePie Sub Count:')
app.addLabel('pSubCountval', '{:,}'.format(pdpCount))
app.addLabel('tSubCountTtl', 'TSeries Sub Count:')
app.addLabel('tSubCountVal', '{:,}'.format(tseriesCount))
app.addLabel('diffTtl', 'Current Difference:')
app.addLabel('diffVal', '{:,}'.format(newCount) + ' (' + str(netChange) + ')')

app.go()