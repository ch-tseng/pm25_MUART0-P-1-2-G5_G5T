#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class pmDataCollect():
    def __init__(self, lengthData, debug=False):
        self.indoorPM1 = []
        self.indoorPM25 = []
        self.indoorPM10 = []
        self.indoorT = []
        self.indoorH = []

        self.outdoorPM1 = []
        self.outdoorPM25 = []
        self.outdoorPM10 = []
        self.outdoorT = []
        self.outdoorH = []

        self.numData = lengthData
        self.voiceFile = ""
        self.displayMode = 0  #0(default), 1 (outdoor), 2(indoor)
        self.displayScreen = 0  #for displayMode=1 or 2, 0: pm1, 1: pm25, 2: pm10

    def dataInput(self, pmType, dataInsert):

        if(pmType == "indoor_pm1"):
            self.indoorPM1.append(dataInsert)
            if(len(self.indoorPM1)>self.numData):
                self.indoorPM1.pop(0)
        elif (pmType == "indoor_pm25"):
            self.indoorPM25.append(dataInsert)
            if(len(self.indoorPM25)>self.numData):
                self.indoorPM25.pop(0)

        elif (pmType == "indoor_pm10"):
            self.indoorPM10.append(dataInsert)
            if(len(self.indoorPM10)>self.numData):
                self.indoorPM10.pop(0)

        elif (pmType == "indoor_T"):
            self.indoorT.append(dataInsert)
            if(len(self.indoorT)>self.numData):
                self.indoorT.pop(0)

        elif (pmType == "indoor_H"):
            self.indoorH.append(dataInsert)
            if(len(self.indoorH)>self.numData):
                self.indoorH.pop(0)


        elif (pmType == "outdoor_pm1"):
            self.outdoorPM1.append(dataInsert)
            if(len(self.outdoorPM1)>self.numData):
                self.outdoorPM1.pop(0)

        elif (pmType == "outdoor_pm25"):
            self.outdoorPM25.append(dataInsert)
            if(len(self.outdoorPM25)>self.numData):
                self.outdoorPM25.pop(0)

        elif (pmType == "outdoor_pm10"):
            self.outdoorPM10.append(dataInsert)
            if(len(self.outdoorPM10)>self.numData):
                self.outdoorPM10.pop(0)

        elif (pmType == "outdoor_T"):
            self.outdoorT.append(dataInsert)
            if(len(self.outdoorT)>self.numData):
                self.outdoorT.pop(0)

        elif (pmType == "outdoor_H"):
            self.outdoorH.append(dataInsert)
            if(len(self.outdoorH)>self.numData):
                self.outdoorH.pop(0)


    def getData(self, pmType):
        if(pmType == "indoor_pm1"):
            return self.indoorPM1

        elif (pmType == "indoor_pm25"):
            return self.indoorPM25

        elif (pmType == "indoor_pm10"):
            return self.indoorPM10

        elif (pmType == "indoor_T"):
            return self.indoorT

        elif (pmType == "outdoor_pm1"):
            return self.outdoorPM1

        elif (pmType == "outdoor_pm25"):
            return self.outdoorPM25

        elif (pmType == "outdoor_pm10"):
            return self.outdoorPM10

        elif (pmType == "outdoor_H"):
            return self.outdoorH


    def getLiveData(self, pmType):
        tmpA = 0
        tmpB = 0

        if(pmType=="pm1"):
            if(len(self.outdoorPM1)>0): tmpA = self.outdoorPM1[-1]
            if(len(self.indoorPM1)>0): tmpB = self.indoorPM1[-1]
            return (tmpA, tmpB)
        elif(pmType=="pm25"):
            if(len(self.outdoorPM25)>0): tmpA = self.outdoorPM25[-1]
            if(len(self.indoorPM25)>0): tmpB = self.indoorPM25[-1]
            return (tmpA, tmpB)
        elif(pmType=="pm10"):
            if(len(self.outdoorPM10)>0): tmpA = self.outdoorPM10[-1]
            if(len(self.indoorPM10)>0): tmpB = self.indoorPM10[-1]
            return (tmpA, tmpB)
        elif(pmType=="T"):
            if(len(self.outdoorT)>0): tmpA = self.outdoorT[-1]
            if(len(self.indoorT)>0): tmpB = self.indoorT[-1]
            return (tmpA, tmpB)
        elif(pmType=="H"):
            if(len(self.outdoorH)>0): tmpA = self.outdoorH[-1]
            if(len(self.indoorH)>0): tmpB = self.indoorH[-1]
            return (tmpA, tmpB)

    def btnSelect(self, btn1, btn2, btn3, btn4):  #btn3--> Default button, btn4 --> Quite button
        self.voiceFile = ""
        if(btn1==1 and btn2==0 and btn3==0 and btn4==0):
            if(self.displayMode != 1):
                self.displayMode = 1
            else:
                self.displayScreen += 1
                if(self.displayScreen>2): self.displayScreen=0

            if(self.displayScreen==0):
                self.voiceFile = "wav/pm1-outdoor.wav"
            elif(self.displayScreen==1):
                self.voiceFile = "wav/pm25-outdoor.wav"
            elif(self.displayScreen==2):
                self.voiceFile = "wav/pm10-outdoor.wav"

        if(btn1==0 and btn2==1 and btn3==0 and btn4==0):
            if(self.displayMode != 2):
                self.displayMode = 2
                self.displayScreen += 1
                if(self.displayScreen>2): self.displayScreen=0
            else:
                self.displayScreen += 1
                if(self.displayScreen>2): self.displayScreen=0

            if(self.displayScreen==0):
                self.voiceFile = "wav/pm1-indoor.wav"
            elif(self.displayScreen==1):
                self.voiceFile = "wav/pm25-indoor.wav"
            elif(self.displayScreen==2):
                self.voiceFile = "wav/pm10-indoor.wav"

        if(btn1==0 and btn2==0 and btn3==1 and btn4==0):
            self.displayMode = 0
            self.voiceFile = "wav/pmstatus.wav"
