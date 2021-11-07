import requests

def getList():
    with open(DIRECTORY + "\\runnersToAdd.txt",'r') as file:
        returnList = []
        line = file.readline()
        while line:
            returnList.append(line[:-1].split(" ")[1])
            line = file.readline()
    return returnList

def saveUserID(Id,name,flag):
    for character in ("_","*","~"):
        if name.find(character) != -1:
            name = '`' + name + '`'
            break
    with open(DIRECTORY + "\\runners.csv",'a') as file:
        file.write(";".join([name,Id,flag]))
        file.write("\n")

def getRunners(): #implement ignore '`'
    with open(DIRECTORY + "\\runners.csv",'r') as file:
        data = []
        line = file.readline()[:-1]
        while line:
            runner,_,_ = line[:-1].split(";")
            data.append(runner.lower())
            line = file.readline()
    return data
    
DIRECTORY = "C:\\Users\\Programador\\Documents\\GitHub\\SrcLbMaker\\SrcLbMaker"
registeredRunners = getRunners()
for name in getList():
    print(name)
    if name.lower() not in registeredRunners:
        data = requests.get("https://www.speedrun.com/api/v1/users/{}".format(name)).json()["data"]
        Id = data["id"]
        if 'country' in data['location']:
            print(data['location']['country']['names']['international'])
            print("flag")
            flag = input()
        saveUserID(data['id'],name,flag)
        registeredRunners.append(name)
    else:
        print("is already in the database")
