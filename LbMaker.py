import requests
import csv
import os
from time import sleep
from time import time

# Util Section #

def apiSleep(text): #to make sure less than 100 request will be made per minute
    begin = time()
    data = requests.get("https://www.speedrun.com/api/v1/" + text).json()["data"]
    end = time()
    timeElapsed = end-begin
    if timeElapsed < 0.6:
        sleep(0.6-timeElapsed)
    return data

def getIDs():
    with open("runners.csv",'r') as file:
        csvReader = csv.reader(file)
        data = {}
        for runner,Id,_ in csvReader:
            data[runner] = Id
    return data

def getFlags():
    with open("runners.csv",'r') as file:
        csvReader = csv.reader(file)
        data = {}
        for runner,_,flag in csvReader:
            data[runner] = flag
    data["Silo_Simon"] = "(deleted) :flag_us:"
    return data

def writeCache(title,data):
    with open("cache.csv",'w') as file:
        csvWriter = csv.writer(file)
        for runner in data:
            csvWriter.writerow([title,runner,data[runner]])

def getCache():
    dataGames = {}
    dataRuns = {}
    dataWrs = {}
    if "cache.csv" in os.listdir():
        datas = {"games":dataGames,"runs":dataRuns,"wrs":dataWrs}
        with open("cache.csv",'r') as file:
            csvReader = csv.reader(file)
            for info,runner,number in csvReader:
                datas[info][runner] = number
    return [dataGames,dataRuns,dataWrs]

# Main Section #

def runsByGuestNA():
    total = 0
    offset = 0
    while True:
        d = apiSleep("runs?guest=N/A&offset={}&max=200".format(offset*200))
        total += len(d)
        if len(d) < 200:
            break
        offset += 1
    return total

def lbData():
    dataGames, dataRuns, dataWrs = getCache()
    try:
        runnerIDs = getIDs()
        for runner in runnerIDs:
            runnerID = runnerIDs[runner]
            if runner in dataWrs:
                print("[cache]{0} : {1} : {2}".format("wrs",runner,data))
            else:
                runs = apiSleep("users/{}/personal-bests?top=1".format(runnerID))
                print(" : ".join(["wrs",runner,str(len(runs))]))
                dataWrs[runner] = len(runs)
            if not((runner in dataRuns) and (runner in dataGames)):
                gamesPlayed = []
                totalRuns = 0
                offset = 0
                while offset*200 < 10000:
                    d = apiSleep("runs?user={0}&offset={1}&max=200&status=verified".format(runnerID,offset*200))
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
        line = "{0}. `{1}` {2} - {3}".format(position - tiedPos,runner,flags[runner],lb[runner])
        print(line)
        text += line + "\n"
        position += 1
    with open("results.txt",'a') as file:
        file.write(text)
    return text

datas = lbData()
for n,data in enumerate(datas):
    print(["\nWRS:\n","\nGAMES:\n","\nRUNS\n"][n])
    if n==2:
        print("-. N/A(guest) :united_nations: : "+str(runsByGuestNA()))
    makeLb(data)
    print()
