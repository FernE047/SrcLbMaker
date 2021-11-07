import srcomapi

def getList(name):
    file = open("C:\\Users\\Programador\\Desktop\\LBot\\" + name + ".txt",'r')
    returnList = []
    line = file.readline()[:-1]
    returnList.append(line.split(" ")[1])
    while line:
        line = file.readline()[:-1]
        if line:
            returnList.append(line.split(" ")[1])
    file.close()
    return returnList

def writeLog(text,user,info):
    file = open("C:\\Users\\Programador\\Desktop\\LBot\\log.txt",'a')
    file.write(" : ".join([text,user,info]))
    file.write("\n")
    print(" : ".join([text,user,info]))
    file.close()

def saveUserID(user,flag,api):
    data = api.get("users/{}".format(user))["id"]
    file = open("C:\\Users\\Programador\\Desktop\\LBot\\users.csv",'a')
    file.write(user + ";" + data + ";" + flag + "\n")
    file.close()
    writeLog("id",user,data)

def exist(name):
    file = open("C:\\Users\\Programador\\Desktop\\LBot\\users.csv",'r')
    data = file.readline()[:-1].split(";")
    if data[0].lower() == name.lower():
        file.close()
        return True
    while data[0]:
        data = file.readline()[:-1].split(";")
        if data[0].lower() == name.lower():
            file.close()
            return True
    return False
    

api = srcomapi.SpeedrunCom();
api.debug = 1
for name in getList("runnersADD"):
    #print("user name")
    #name = input()
    print(name)
    if not exist(name):
        print("flag")
        flag = input()
        saveUserID(name,flag,api)
    else:
        print("it's already in the database")
