import requests

def getList():
    with open("runnersToAdd.txt",'r') as file:
        returnList = []
        line = file.readline()
        while line:
            returnList.append(line[:-1].split(" ")[1])
            line = file.readline()
    return returnList

def saveUserID(Id,name,flag):
    with open("runners.csv",'a') as file:
        csvWriter = csv.writer(file)
        csvWriter.writerow([name,Id,flag])

def getRunners():
    with open("runners.csv",'r') as file:
        csvReader = csv.reader(file)
        data = []
        for runner,_,_ in csvReader:
            data.append(runner.lower())
    return data
    
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
