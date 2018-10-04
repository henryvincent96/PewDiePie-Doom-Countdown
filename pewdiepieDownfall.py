import urllib.request
import json
import time
import platform
from os import system

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

#init
clearScreenCommand = setClearScreenCommand()
pdpCount = 0
tseriesCount = 0
netChange = 0
previousCount = 0
newCount = getCountdown()

#main loop
while True:
    #logic
    try:
        previousCount = newCount
        newCount = getCountdown()
        netChange = newCount - previousCount

        if netChange >= 0:
            netChange = str('+' + str(netChange))
        #output
        _ = system(clearScreenCommand)
        print('PewDiePie Sub Count: ' + '{:,}'.format(pdpCount))
        print('T Series Sub Count: ' + '{:,}'.format(tseriesCount))
        print('Current Difference: ' + '{:,}'.format(newCount)+ ' (' + str(netChange) +')')
    except TimeoutError:
        print('Timeout error')
    except urllib.error.URLError:
        print('URL error')
    #don't really want google thinking I'm DDOSing them
    time.sleep(1)