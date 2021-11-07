import srcomapi
from time import sleep
from time import time
from textos import embelezeTempo as eT

# Util Section #

def apiSleep(api,text):
    begin = time()
    data = api.get(text)
    end = time()
    timeElapsed = end-begin
    if timeElapsed < 0.6:
        sleep(0.6-timeElapsed)
    return data

def getList(name):
    file = open(DIRECTORY + "\\" + name + ".csv",'r')
    returnList = []
    line = file.readline()[:-1]
    returnList.append(line.split(";")[0])
    while line:
        line = file.readline()[:-1]
        if line:
            returnList.append(line.split(";")[0])
    file.close()
    return returnList

def userId(user,api):
    file = open(DIRECTORY + "\\users.csv",'r')
    data = file.readline()[:-1].split(";")
    if data[0].lower() == user.lower():
        file.close()
        return data[1]
    while data[0]:
        data = file.readline()[:-1].split(";")
        if data[0] == user:
            file.close()
            return data[1]

def writeLog(text,user,info):
    file = open(DIRECTORY + "\\log.txt",'a')
    file.write(" : ".join([text,user,info]))
    file.write("\n")
    print(" : ".join([text,user,info]))
    file.close()

def getFlag(user):
    if user in ["(guest) N/A","(guest) n/a"]:
        return ":united_nations:"
    if user == "Silo_Simon":
        return "(deleted) :flag_us:"
    file = open(DIRECTORY + "\\users.csv",'r')
    data = file.readline()[:-1].split(";")
    if data[0].lower() == user.lower():
        file.close()
        return data[2]
    while data[0]:
        data = file.readline()[:-1].split(";")
        if data[0].lower() == user.lower():
            file.close()
            return data[2]

def getLog(user,info):
    file = open(DIRECTORY + "\\log.txt",'r')
    line = file.readline()[:-1]
    while line:
        line = line.split(" : ")
        if user == line[1]:
            if line[0] == info:
                file.close()
                return int(line[2])
        line = file.readline()[:-1]
    file.close()
    return False

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
    datawrs = {}
    datagames = {}
    dataruns = {}
    for runner in getList("users"):
        data = getLog(runner,"wrs")
        runnerID = userId(runner,api)
        if data:
            datawrs[runner] = int(data)
            print("[LOG]{0} : {1} : {2}".format("wrs",runner,data))
        else:
            runs = apiSleep(api,"users/{}/personal-bests?top=1".format(runnerID))
            writeLog("wrs",runner,str(len(runs)))
            datawrs[runner] = len(runs)

        searchNeeded = False
        
        data = getLog(runner,"runs")
        if data:
            dataruns[runner] = data
        else:
            searchNeeded = True

        data = getLog(runner,"games")
        if data:
            datagames[runner] = data
        else:
            searchNeeded = True
        
        if searchNeeded:
            gamesPlayed = []
            total = 0
            offset = 0
            while True:
                d = apiSleep(api,"runs?user={0}&offset={1}&max=200&status=verified".format(runnerID,offset*200))
                total += len(d)
                for run in d:
                    if run["game"] not in gamesPlayed:
                        gamesPlayed.append(run["game"])
                if len(d) < 200:
                    break
                offset += 1
            writeLog("runs",runner,str(total))
            writeLog("games",runner,str(len(gamesPlayed)))
            
            dataruns[runner] = total
            datagames[runner] = len(gamesPlayed)
        else:
            print("[LOG]{0} : {1} : {2}".format("runs",runner,dataruns[runner]))
            print("[LOG]{0} : {1} : {2}".format("games",runner,datagames[runner]))
    datagames["Silo_Simon"] = 123
    return (datawrs,datagames,dataruns)

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
        line = "{0}. {1} {2} - {3}".format(position - tiedPos,runner,getFlag(runner),lb[runner])
        print(line)
        text += line + "\n"
        position += 1
    file = open(DIRECTORY + "\\results.txt",'a')
    file.write(text)
    file.close()
    return text

DIRECTORY = "C:\\Users\\Programador\\Documents\\GitHub\\SrcLbMaker\\SrcLbMaker"
a = time()
api = srcomapi.SpeedrunCom();
api.debug = 0
datas = lbData(api)
for n,data in enumerate(datas):
    print(["\nWRS:\n","\nGAMES:\n","\nRUNS\n"][n])
    if n==2:
        print("guest : "+str(runsByGuestNA()))
    makeLb(data)
    print()
b = time()
print(eT(b-a))
