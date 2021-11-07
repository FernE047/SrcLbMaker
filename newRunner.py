import requests

def getList(name):
    with open(DIRECTORY + "\\runnersToAdd.txt",'r') as file:
        returnList = []
        line = file.readline()[:-1]
        while line:
            returnList.append(line.split(" ")[:-1][1])
            line = file.readline()
    return returnList

def saveUserID(name,flag):
    data = requests.get("users/{}".format(name)).json()["data"]["id"]
    with open(DIRECTORY + "\\runners.csv",'a') as file:
        file.write(";".join([user,data,flag]))
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
