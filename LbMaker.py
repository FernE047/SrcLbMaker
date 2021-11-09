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

def getRunnerInfo():
    with open("runners.csv",'r') as file:
        csvReader = csv.DictReader(file)
        data = {}
        for info in csvReader:
            data[info['name']] = info
    return data

def writeCache(runners):
    with open("cache.csv",'w') as file:
        csvWriter = csv.writer(file)
        for runner in list(runners.values()):
            for cat in ["wrs","runs","games"]:
                if cat not in runner:
                    runner[cat] = ''
            csvWriter.writerow([runner["name"],runner["games"],runner["runs"],runner["wrs"]])

def getCache(runners):
    if "cache.csv" in os.listdir():
        with open("cache.csv",'r') as file:
            csvReader = csv.reader(file)
            for name,games,runs,wrs in csvReader:
                if games:
                    runners[runner]['games'] = games
                if runs:
                    runners[runner]['runs'] = runs
                if wrs:
                    runners[runner]['wrs'] = wrs

# Main Section #

def lbData():
    runners = getRunnerInfo() #implement classes
    getCache(runners)
    try:
        for runner in list(runners.values()):
            if ("runs" in runner) and ("games" in runner):
                print("[cache]{0} : {1} : {2}".format("runs",runner['name'],runner['runs']))
                print("[cache]{0} : {1} : {2}".format("games",runner['name'],runner['games']))
            else:
                if not runner["id"]:
                    search = "runs?guest=" + runner["name"] + "&offset={}&max=200&status=verified"
                    runner["name"] += " (guest)"
                else:
                    search = "runs?user=" + runner["id"] + "&offset={}&max=200&status=verified"
                gamesPlayed = []
                totalRuns = 0
                offset = 0
                while offset*200 < 10000:
                    runs = apiSleep(search.format(offset*200))
                    totalRuns += len(runs)
                    for run in runs:
                        if run["game"] not in gamesPlayed:
                            gamesPlayed.append(run["game"])
                    if len(runs) < 200:
                        break
                    offset += 1
                if offset*200==10000:
                    print("implement backwards search for runner : " + runner)
                    raise Exception("implement backwards search for runner : " + runner)
                print(" : ".join(["games",runner["name"],str(len(gamesPlayed))]))
                print(" : ".join(["runs",runner["name"],str(totalRuns)]))
                runner["runs"] = totalRuns
                runner["games"] = len(gamesPlayed)
            if "wrs" in runner:
                print("[cache]{0} : {1} : {2}".format("wrs",runner['name'],data))
            else:
                if runner["id"]:
                    runs = apiSleep("users/{}/personal-bests?top=1".format(runner["id"]))
                    print(" : ".join(["wrs",runner['name'],str(len(runs))]))
                    runner['wrs'] = len(runs)
        runners["Silo_Simon"] = {"name":"Silo_Simon (deleted)", "id":"zxz9ppr8", "flag":":flag_us:","games":123}
        writeCache(runners)
        return runners
    except:
        writeCache(runners)

def lbOrder(runners,info):
    lbNumbers = []
    for runner in list(runners.values()):
        if info in runner:
            if runner[info] not in lbNumbers:
                lbNumbers.append(runner[info])
    lbNumbers.sort()
    lbNumbers = reversed(lbNumbers)
    lbRunners = []
    for number in lbNumbers:
        for runner in list(runners.values()):
            if info in runner:
                if runner[info] == number:
                    lbRunners.append(runner)
    return lbRunners

def makeLb(runners,info):
    lbRunners = lbOrder(runners,info)
    position = 1
    tiedPos = 0
    with open("results.txt",'a') as file:
        for i in range(len(lbRunners)):
            runner = lbRunners[i]
            if "id" not in runner:
                line = "`{0: 3d}`.{1}`{2} - {3: 5d}`".format("-",
                                                             runner["flag"],
                                                             " "*(25-len(runner['name'])) + runner['name'],
                                                             runner[info])
            else:
                if i != 0:
                    if runner[info] == lbRunners[i-1][info]:
                        tiedPos += 1
                    else:
                        tiedPos = 0
                line = "`{0: 3d}.`{1}`{2} - {3: 5d}`".format(position - tiedPos,
                                                             runner["flag"],
                                                             " "*(25-len(runner['name'])) + runner['name'],
                                                             runner[info])
                position += 1
            print(line)
            file.write(line+"\n")

runners = lbData()
for info in ("games","runs","wrs"):
    print(info.upper(),end = "\n\n")
    makeLb(runners,info)
    print("\n")
