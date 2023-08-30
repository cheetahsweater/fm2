import os
path = os.getcwd()

filelist = os.listdir()

def tobool(value):
    if int(value) == 0:
            newValue = False
    elif int(value) == 1:
        newValue = True
    else:
        raise ValueError("Value not 0 or 1 (not bool)")
    return newValue

def controls(value):
    if int(value) == 0:
            newValue = "none"
    elif int(value) == 1:
        newValue = "gamepad"
    elif int(value) == 2:
        newValue = "zapper"
    else:
        raise ValueError("Value not 0 or 1 (not bool)")
    return newValue
     

def readfm2(file):
    with open(f"{path}\\{file}","r") as file:
        lines = []
        text = file.readlines()
        for line in text:
            lines.append(line.removesuffix("\n"))
        fm2 = dict()
        #Version of the movie - ALWAYS 3
        fm2.update({"version": lines[0].strip("version ")})

        #Emulator version used to record movie
        fm2.update({"emulatorVersion": lines[1].removeprefix("emuVersion ")})

        #Rerecord count (self-explanatory)
        fm2.update({"rerecordCount": lines[2].removeprefix("rerecordCount ")}) 

        #Whether or not the movie uses PAL timing (boolean)
        fm2.update({"palFlag": lines[3].removeprefix("palFlag ")}) 
        fm2["palFlag"] = tobool(fm2["palFlag"])

        #Filename of ROM being played
        fm2.update({"romFilename": lines[4].removeprefix("romFilename ")})

        #The base64 of the hexified MD5 hash of the ROM which was used to record the movie (I don't know)
        fm2.update({"romChecksum": lines[5].removeprefix("romChecksum ")})

        #Movie ID used for loading savestates, not necessarily relevant here but good to have
        fm2.update({"guid": lines[6].removeprefix("guid ")})

        #Whether or not a fourscore was used (boolean)
        fm2.update({"fourscore": lines[7].removeprefix("fourscore ")})
        fm2["fourscore"] = tobool(fm2["fourscore"])

        #Whether or not a microphone was used (boolean)
        #Note: This line is not covered in the FCEUX documentation so I assume it is obsolete, but including anyway
        fm2.update({"microphone": lines[8].removeprefix("microphone ")})
        fm2["microphone"] = tobool(fm2["microphone"])

        #Indicates controller used in port 0 (see function "controls" for more details)
        fm2.update({"port0": lines[9].removeprefix("port0 ")})
        fm2["port0"] = controls(fm2["port0"])

        #print(lines[9])
        print(fm2)

readfm2("duma.fm2")
readfm2("Somari.fm2")
readfm2("7-in-1.fm2")