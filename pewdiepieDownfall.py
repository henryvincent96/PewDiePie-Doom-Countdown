import urllib.request
import json
import time
import datetime
from os import system

#gets sub count from youtube for a given channel ID
def getSubCount(id):
    data = urllib.request.urlopen("https://www.googleapis.com/youtube/v3/channels?part=statistics&id=" + id + "&key=" + key).read()
    return json.loads(data)["items"][0]["statistics"]["subscriberCount"]

#Calculates the difference between PewDiePie and T Series
#For optimisation, sub counts are global variables
def getCountdown():
    global pdpCount, tseriesCount
    pdpCount = int(getSubCount(pdpID))
    tseriesCount = int(getSubCount(tseriesID))
    return pdpCount - tseriesCount

#variables required for API
key = "AIzaSyBR7ZQmh02ETze1hjNS7rFYsSJSBYoUsvY"
pdpID = "UC-lHJZR3Gqxm24_Vd_AJ5Yw"
tseriesID = "UCq-Fj5jknLsUf-MWSy4_brA"

#init
pdpCount = 0
tseriesCount = 0
netChange = 0
previousCount = 0
newCount = getCountdown()
timeAtStart = datetime.datetime.now()

#main loop
while True:
    #logic
    try:
        previousCount = newCount
        newCount = getCountdown()
        netChange += newCount - previousCount
        delta = datetime.datetime.now() - timeAtStart
        #output
        _ = system('cls')
        print("PewDiePie Sub Count: " + str(pdpCount))
        print("T Series Sub Count: " + str(tseriesCount))
        print("Current Difference: " + str(newCount))
        print("Net Change Since Launch: " + str(netChange))
        print("Time Recorded: " + str(delta))
    except TimeoutError:
        print("Timeout error")
    except urllib.error.URLError:
        print("URL error")
    #don't really want google thinking I'm DDOSing them
    time.sleep(1)