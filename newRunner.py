import requests

def getList():
    with open(DIRECTORY + "\\runnersToAdd.txt",'r') as file:
        returnList = []
        line = file.readline()
        while line:
            returnList.append(line[:-1].split(" ")[1])
            line = file.readline()
    return returnList

def saveUserID(name,flag):
    data = requests.get("https://www.speedrun.com/api/v1/users/{}".format(name)).json()["data"]["id"]
    with open(DIRECTORY + "\\runners.csv",'a') as file:
        file.write(";".join([name,data,flag]))
        file.write("\n")

def getRunners():
    with open(DIRECTORY + "\\runners.csv",'r') as file:
        data = []
        line = file.readline()[:-1]
        while line:
            runner,_,_ = line[:-1].split(";")
            data.append(runner)
            line = file.readline()
    return data
    
DIRECTORY = "C:\\Users\\Programador\\Documents\\GitHub\\SrcLbMaker\\SrcLbMaker"
registeredRunners = getRunners()
for name in getList():
    print(name)
    if name not in registeredRunners:
        print("flag")
        flag = input()
        saveUserID(name,flag)
    else:
        print("is already in the database")
