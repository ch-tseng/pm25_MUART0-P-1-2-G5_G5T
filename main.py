import time, os
import RPi.GPIO as GPIO
#from libraryCH.database.sqlite import sqlitedb
from libMUART.device.air import G5
from libMUART.device.lcd import ILI9341
from libMUART.app.MUART0P12 import pmDataCollect
from subprocess import call

#Set the volume to 100%
call(["amixer", "sset", "PCM,0", "100%"])

#Configurable, you can update the parameter's value below
debug=0  #change to 1 will display more messasge for debug
pinDevice = 2  #the GPIO pin which will switch RF Uart device #1 and #2
pinPIR = 4  #the GPIO pin for PIR module
pinOutdoor = 21  #the GPIO pin for the button of outdoor's pm25 display
pinIndoor = 20  #the GPIO pin for the button of indoor's pm25 display
pinDefault = 16  #the GPIO pin for the button of default pm25 display
pinQuite = 12  # disable the speak sound for PIR

#--> Not used....
outdoor_pm25model = "G"  #You can select G or GT or GTS. (G: only pm2.5, GT: pm2.5+T&H, GTS: pm2.5+T&H+gas)
indoor_pm25model = "GT" #You can select G or GT or GTS. (G: only pm2.5, GT: pm2.5+T&H, GTS: pm2.5+T&H+gas)
#<---

sensorRefresh = 15  #This number must be odd number, how many seconds will re-read the sensor data? 
numData = 46  #How many pm25 data will be displayed on the screen?
pirSensity = 3  #Sensity for the PIR, large number will delay the PIR sensity

#you don't have to change the values below
a_pm1 = [0, 0, 0, 0, 0, 0]
a_pm25 = [0, 0, 0, 0, 0, 0]
a_pm10 = [0, 0, 0, 0, 0, 0]
setVoice = True
setScreen = 0
#displayMode = 0  #0(default), 1 (outdoor), 2(indoor)
#displayScreen = 0  #for displayMode=1 or 2, 0: pm1, 1: pm25, 2: pm10
lastPlayVoice = 0
pirAccumulated = 0
last_pinOutdoor = 1
last_pinIndoor = 1
last_pinDefault = 1
last_pinQuite = 1
deviceID = 0  # which sensor (#1, #2) is connected now ?

speaker = False   #Speaker on or off
bg = "pics/pmbg2.jpg"

#Setup
#You have to update the LCD's siae and rotation if the LCD is not 240x320 resolution
lcd = ILI9341(LCD_size_w=240, LCD_size_h=320, LCD_Rotate=0)
lcd.displayImg(bg)
time.sleep(1)

GPIO.setmode(GPIO.BCM)
GPIO.setup(pinDevice ,GPIO.OUT)
GPIO.output(pinDevice, GPIO.LOW)
GPIO.setup(pinPIR ,GPIO.IN)
#GPIO.setup(pinOutdoor ,GPIO.IN)
#GPIO.setup(pinIndoor ,GPIO.IN)
GPIO.setup(pinOutdoor, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(pinIndoor, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(pinDefault, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(pinQuite, GPIO.IN, pull_up_down=GPIO.PUD_UP)

dataPM = pmDataCollect(lengthData=numData, debug=False)
#dataPM.displayMode = 0  #0(default), 1 (outdoor), 2(indoor)
#dataPM.displayScreen = 9  #for displayMode=1 or 2, 0: pm1, 1: pm25, 2: pm10

def readFromUart(delay=0.2):
    g3 = (air.read("/dev/ttyS0"))
    #print("try to read second")
    time.sleep(delay)
    #print("try to third second")
    #We only use the second data of reading
    g3 = (air.read("/dev/ttyS0"))

    try:
        pm1 = g3[3]
    except:
        pm1 = 0

    try:
        pm10 = g3[4]
    except:
        pm10 = 0

    try:
        pm25 = g3[5]
    except:
        pm25 = 0

    try:
        T = g3[6]
    except:
        T = 0

    try:
        H = g3[7]
    except:
        H = 0


    return (pm1, pm10, pm25, T, H)

air=G5()
air.debug = False
i = 0
while True:
    pirStatus = GPIO.input(pinPIR)
    btn1 = GPIO.input(pinOutdoor)
    btn2 = GPIO.input(pinIndoor)
    btn3 = GPIO.input(pinDefault)
    btn4 = GPIO.input(pinQuite)
    #print("PIR:{}  BTN1:{}  BTN2:{}  mainBTN:{}  quiteBTN:{}".format(pirStatus, btn1,btn2,btn3, btn4))

    if(btn3!=last_pinDefault and btn3==0):
        #print("Default Button clicked")
        dataPM.btnSelect(0, 0, 1, 0)

    if((btn1!=last_pinOutdoor and btn1==0) and (btn2!=last_pinIndoor and btn2==0)):
        #print("BTN1,2 clicked")
        lcd.displayImg("pics/poweroff.jpg")
        os.system('sudo shutdown now')

    else:
        if(btn1!=last_pinOutdoor and btn1==0):
            #print("BTN1 clicked")
            dataPM.btnSelect(1, 0, 0, 0)
        if(btn2!=last_pinIndoor and btn2==0):
            #print("BTN2 clicked")
            dataPM.btnSelect(0, 1, 0, 0)

    if(btn4==0 and btn4!=last_pinQuite):
        if(speaker==True):
            bg = "pics/pmbg2.jpg"
            speaker = False
        else:
            bg = "pics/pmbg.jpg"
            speaker = True
            if(speaker==True):
                os.system('omxplayer --no-osd wav/speakeron.wav')

    last_pinIndoor = btn2
    last_pinOutdoor = btn1
    last_pinDefault = btn3
    last_pinQuite = btn4

    if(dataPM.displayMode==0):
        lcd.printSensordata("e1.ttf", pmT=dataPM.getLiveData("T"), pm25=dataPM.getLiveData("pm25"), \
                pm1=dataPM.getLiveData("pm1"), pm10=dataPM.getLiveData("pm10"), \
                pmH=dataPM.getLiveData("H"), imagePath=bg)

    elif(dataPM.displayMode==1):
        if(dataPM.displayScreen==0):
            lcd.drawLineChart(dataPM.getData("outdoor_pm1"), "e1.ttf", "pics/outdoor_pm1.jpg")
        elif(dataPM.displayScreen==1):
            lcd.drawLineChart(dataPM.getData("outdoor_pm25"), "e1.ttf", "pics/outdoor_pm25.jpg")
        elif(dataPM.displayScreen==2):
            lcd.drawLineChart(dataPM.getData("outdoor_pm10"), "e1.ttf", "pics/outdoor_pm10.jpg")

    elif(dataPM.displayMode==2):
        if(dataPM.displayScreen==0):
            lcd.drawLineChart(dataPM.getData("indoor_pm1"), "e1.ttf", "pics/indoor_pm1.jpg")
        elif(dataPM.displayScreen==1):
            #print(dataPM.getData("indoor_pm25"))
            lcd.drawLineChart(dataPM.getData("indoor_pm25"), "e1.ttf", "pics/indoor_pm25.jpg")
        elif(dataPM.displayScreen==2):
            lcd.drawLineChart(dataPM.getData("indoor_pm10"), "e1.ttf", "pics/indoor_pm10.jpg")

    if(dataPM.voiceFile != ""): 
        if(speaker==True):
            os.system('omxplayer --no-osd ' + dataPM.voiceFile )

        dataPM.voiceFile  = ""

    #print(" i={}, i % sensorRefresh={} ".format(i,(i % sensorRefresh)))
    if(i % sensorRefresh == 0):
        if(i % 2 == 0):
            GPIO.output(pinDevice, GPIO.LOW)
            print("read Sensor #2")
            deviceID = 0
            liveData = readFromUart(0.2)

            dataPM.dataInput("indoor_pm1", liveData[0])
            dataPM.dataInput("indoor_pm25", liveData[2])
            dataPM.dataInput("indoor_pm10", liveData[1])
            #dataPM.dataInput("indoor_T", round(liveData[3],0))
            #dataPM.dataInput("indoor_H", round(liveData[4],0))

            if(i>100): i=0
        else:
            GPIO.output(pinDevice, GPIO.HIGH)
            print("read Sensor #1")
            deviceID = 1
            liveData = readFromUart(0.2)

            dataPM.dataInput("outdoor_pm1", liveData[0])
            dataPM.dataInput("outdoor_pm25", liveData[2])
            dataPM.dataInput("outdoor_pm10", liveData[1])
            dataPM.dataInput("outdoor_T", round(liveData[3],0))
            dataPM.dataInput("outdoor_H", round(liveData[4],0))


        print ("time:{} PIR:{} BTN1:{} BTN2:{} device:{} --> pm1:{} pm2.5:{} pm10:{}".format(round(time.time()-lastPlayVoice),\
                pirStatus, btn1, btn2, deviceID, liveData[0], liveData[2], liveData[1]))


    if(pirStatus==1): 
        pirAccumulated += 1
    else:
        pirAccumulated = 0

    if(pirAccumulated>pirSensity and i>0 and time.time()-lastPlayVoice>60):
        pirAccumulated = 0

        if(liveData[2]<=50):
            wav = 'pm25_1.wav'
        elif(liveData[2]>50 and liveData[2]<=100):
            wav = 'pm25_2.wav'
        elif(liveData[2]>100 and liveData[2]<=150):
            wav = 'pm25_3.wav'
        elif(liveData[2]>150 and liveData[2]<=200):
            wav = 'pm25_4.wav'
        elif(liveData[2]>200 and liveData[2]<=300):
            wav = 'pm25_5.wav'
        elif(liveData[2]>300):
            wav = 'pm25_6.wav'

        if(speaker==True):
            os.system('omxplayer --no-osd wav/' + wav)

        lastPlayVoice = time.time()

    i += 1
