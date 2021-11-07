import srcomapi
import requests
import os
from time import sleep
from time import time

# Util Section #

def apiSleep(api,text):
    begin = time()
    data = requests.get(text).json()["data"]
    end = time()
    timeElapsed = end-begin
    if timeElapsed < 0.6:
        sleep(0.6-timeElapsed)
    return data

def getIDs():
    with open(DIRECTORY + "\\runners.csv",'r') as file:
        data = {}
        line = file.readline()[:-1]
        while line:
            runner,Id,_ = line[:-1].split(";")
            data[runner] = Id
            line = file.readline()
    return data

def getFlags():
    with open(DIRECTORY + "\\runners.csv",'r') as file:
        data = {}
        line = file.readline()[:-1]
        while line:
            runner,_,flag = line[:-1].split(";")
            data[runner] = flag
            line = file.readline()
    data["Silo_Simon"] = "(deleted) :flag_us:"
    return data

def writeCache(title,data):
    with open(DIRECTORY + "\\cache.csv",'r') as file:
        for runner in data:
            file.write(";".join([title,runner,data[runner]]))
            file.write("\n")

def getCache():
    dataGames = {}
    dataRuns = {}
    dataWrs = {}
    datas = {"games":dataGames,"runs":dataRuns,"wrs":dataWrs}
    if "cache.csv" in os.listdir(DIRECTORY):
        with open(DIRECTORY + "\\cache.csv",'r') as file:
            line = file.readline()[:-1]
            while line:
                info,runner,number = line.split(";")
                datas[info][runner] = number
    return [dataGames,dataRuns,dataWrs]

# API Section #

def runsByGuestNA():
    total = 0
    offset = 0
    while True:
        d = apiSleep(api,"runs?guest=N/A&offset={}&max=200".format(offset*200))
        total += len(d)
        if len(d) < 200:
            break
        offset += 1
    return total

def lbData(api):
    dataGames, dataRuns, dataWrs = getCache()
    try:
        runnerIDs = getIDs()
        for runner in runnerIDs:
            runnerID = runnerIDs[runner]
            if runner in dataWrs:
                print("[cache]{0} : {1} : {2}".format("wrs",runner,data))
            else:
                runs = apiSleep(api,"users/{}/personal-bests?top=1".format(runnerID))
                print(" : ".join(["wrs",runner,str(len(runs))]))
                dataWrs[runner] = len(runs)
            if not((runner in dataRuns) and (runner in dataGames)):
                gamesPlayed = []
                totalRuns = 0
                offset = 0
                while offset*200 < 10000:
                    d = apiSleep(api,"runs?user={0}&offset={1}&max=200&status=verified".format(runnerID,offset*200))
                    totalRuns += len(d)
                    for run in d:
                        if run["game"] not in gamesPlayed:
                            gamesPlayed.append(run["game"])
                    if len(d) < 200:
                        break
                    offset += 1
                if offset*200==10000:
                    print("implement backwards search for runner : " + runner)
                    raise Exception("implement backwards search for runner : " + runner)
                print(" : ".join(["runs",runner,str(totalRuns)]))
                print(" : ".join(["games",runner,str(len(gamesPlayed))]))
                
                dataRuns[runner] = totalRuns
                dataGames[runner] = len(gamesPlayed)
            else:
                print("[cache]{0} : {1} : {2}".format("runs",runner,dataRuns[runner]))
                print("[cache]{0} : {1} : {2}".format("games",runner,dataGames[runner]))
        dataGames["Silo_Simon"] = 123
        return (dataWrs,dataGames,dataRuns)
    except:
        writeCache("wrs",dataWrs)
        writeCache("runs",dataRuns)
        writeCache("games",dataGames)

def lbOrder(data):
    lbNumbers = list(data.values())
    lbNumbers.sort()
    lbNumbers = reversed(lbNumbers)
    lbRunners = []
    lb = {}
    for number in lbNumbers:
        for runner in data:
            if data[runner] == number:
                break
        lb[runner] = data.pop(runner)
        lbRunners.append(runner)
    return lbRunners,lb

def makeLb(data):
    lbRunners,lb = lbOrder(data)
    flags = getFlags()
    position = 1
    tiedPos = 0
    text = ""
    for i in range(len(lbRunners)):
        runner = lbRunners[i]
        if i != 0:
            if lb[runner] == lb[lbRunners[i-1]]:
                tiedPos += 1
            else:
                tiedPos = 0
        line = "{0}. {1} {2} - {3}".format(position - tiedPos,runner,flags[runner],lb[runner])
        print(line)
        text += line + "\n"
        position += 1
    with open(DIRECTORY + "\\results.txt",'a') as file:
        file.write(text)
    return text

DIRECTORY = "C:\\Users\\Programador\\Documents\\GitHub\\SrcLbMaker\\SrcLbMaker"
datas = lbData(api)
for n,data in enumerate(datas):
    print(["\nWRS:\n","\nGAMES:\n","\nRUNS\n"][n])
    if n==2:
        print("-. N/A(guest) :united_nations: : "+str(runsByGuestNA()))
    makeLb(data)
    print()
