import os
import json
path = os.getcwd()
filelist = os.listdir(f"{path}\\fm2")

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
     

def readfm2(filename):
    with open(f"{path}\\fm2\\{filename}","r") as file:
        lines = []
        text = file.readlines()
        for line in text:
            lines.append(line.removesuffix("\n"))
        fm2 = dict()
        movelist = []
        #Version of the movie - ALWAYS 3
        for line in lines:
            if line[:7] == "version":    
                fm2.update({"version": line.strip("version ")})

            #Emulator version used to record movie
            if line[:10] == "emuVersion":
                fm2.update({"emulatorVersion": line.removeprefix("emuVersion ")})

            #Rerecord count (self-explanatory)
            if line[:13] == "rerecordCount":
                fm2.update({"rerecordCount": line.removeprefix("rerecordCount ")}) 

            #Whether or not the movie uses PAL timing (boolean)
            if line[:7] == "palFlag":
                fm2.update({"palFlag": line.removeprefix("palFlag ")}) 
                fm2["palFlag"] = tobool(fm2["palFlag"])

            #Filename of ROM being played
            if line[:11] == "romFilename":
                fm2.update({"romFilename": line.removeprefix("romFilename ")})

            #The base64 of the hexified MD5 hash of the ROM which was used to record the movie (I don't know)
            if line[:11] == "romChecksum":
                fm2.update({"romChecksum": line.removeprefix("romChecksum ")})

            #Movie ID used for loading savestates, not necessarily relevant here but good to have
            if line[:4] == "guid":
                fm2.update({"guid": line.removeprefix("guid ")})

            #Whether or not a fourscore was used (boolean)
            if line[:9] == "fourscore":
                fm2.update({"fourscore": line.removeprefix("fourscore ")})
                fm2["fourscore"] = tobool(fm2["fourscore"])

            #Whether or not a microphone was used (boolean)
            #Note: This line is not covered in the FCEUX documentation so I assume it is obsolete, but including anyway
            if line[:10] == "microphone":
                fm2.update({"microphone": line.removeprefix("microphone ")})
                fm2["microphone"] = tobool(fm2["microphone"])

            #Indicates controller used in port 0 (see function "controls" for more details)
            if line[:5] == "port0":
                fm2.update({"port0": line.removeprefix("port0 ")})
                fm2["port0"] = controls(fm2["port0"])

            #Indicates controller used in port 1 (see function "controls" for more details)
            if line[:5] == "port1":
                fm2.update({"port1": line.removeprefix("port1 ")})
                fm2["port1"] = controls(fm2["port1"])

            #Indicates type of FCExp port attached, only supported value is 0
            if line[:5] == "port2":
                fm2.update({"port2": line.removeprefix("port2 ")})

            #Whether or not movie was recorded for a Famicom Disk System game
            if line[:3] == "FDS":
                fm2.update({"FDS": line.removeprefix("FDS ")})
                fm2["FDS"] = tobool(fm2["FDS"])

            #Whether or not movie uses NewPPU 
            #(FCEUX 2.1.2 onwards have this option, but according to their site it is slower so unlikely)
            if line[:6] == "NewPPU":
                fm2.update({"NewPPU": line.removeprefix("NewPPU ")})
                fm2["NewPPU"] = tobool(fm2["NewPPU"])

            #Whether or not movie uses RAM initialization
            if line[:13] == "RAMInitOption":
                fm2.update({"RAMInitOption": line.removeprefix("RAMInitOption ")})
                fm2["RAMInitOption"] = tobool(fm2["RAMInitOption"])

            #Seed for RAM initialization
            if line[:11] == "RAMInitSeed":
                fm2.update({"RAMInitSeed": line.removeprefix("RAMInitSeed ")})

            if line[:10] == "savestate ":
                fm2.update({"savestate": line.removeprefix("savestate ")})

            if line[:6] == "binary":
                fm2.update({"binary": line.removeprefix("binary ")})
                fm2["binary"] = tobool(fm2["binary"])
            
            if line[:6] == "length":
                fm2.update({"length": line.removeprefix("length ")})
                fm2["length"] = tobool(fm2["length"])
            
            if line[:7] == "comment":
                fm2.update({"comment": line.removeprefix("comment ")})
            
            if line[:8] == "subtitle":
                fm2.update({"subtitle": line.removeprefix("subtitle ")})

            else:
                movelist.append(line)
        print(len(movelist))
        print(movelist[-310:-300])
        rawfilename = filename.removesuffix(".fm2")
        with open(f"{path}\\{rawfilename}_info.json","w") as file:
            myjson = json.dumps(fm2)
            file.write(myjson)
            print(f"{rawfilename}_info.json written.")
        

for file in filelist:
    if file[-4:] == ".fm2":
        readfm2(file)