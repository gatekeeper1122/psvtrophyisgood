import binascii
import ParseTRPSFM
import ParseTRPTITLE
def init(path):
    global trpData
    global readPath
    readPath = path
    trpData = open(path, "rb").read()

def getAccountId():
    return binascii.hexlify(trpData[0x120:0x120+0x8])

def makeCmaAid(aid):
    cmaAid = [aid[i:i + 2] for i in range(0, len(aid), 2)]
    cmaAid.reverse()
    return str(cmaAid)

def getNumberOfUnlockedTrophies():
    return int(str(binascii.hexlify(trpData[0x187:0x188])),16)

def setNumberOfUnlockedTrophies(unlockedTrophys):
    if unlockedTrophys > 0xFF & unlockedTrophys < 0x00:
        return "Too Long!"
    numToWrite = hex(unlockedTrophys)[3:]
    if numToWrite.endswith("L"):
        numToWrite = numToWrite[:-1]
    if len(numToWrite) == 1:
        numToWrite = "0" + numToWrite
    trpData = binascii.hexlify(open(readPath, "rb").read())
    a = trpData[:782]
    b = trpData[784:]
    trpData = a+numToWrite+b
    open(readPath, "wb").write(binascii.unhexlify(trpData))


def getNpCommId():
    return trpData[0x170:0x170 + 0x0C]

def getNpCommSign():
    return binascii.hexlify(trpData[400:560])

def findDataZone(v):
        begin = 0x2B7
        end = begin + 0xAC
        a = 0
        while a != v:
            begin += 0xb0
            end = begin + 0xAC
            a += 1
        return {"begin":begin,"end":end}

def getTrophyDataBlock(v):
    begin = findDataZone(v)["begin"]
    end = findDataZone(v)["end"]
    print "Begin: "+str(begin)
    print "End: " + str(end)
    print "trophyId: "+str(v)
    print binascii.hexlify(trpData[begin:end])
    return binascii.hexlify(trpData[begin:end])

def writeTimestamp(v,timestamp):
    dataBlock = getTrophyDataBlock(v)
    a = dataBlock[:52]
    b = dataBlock[82:]
    newDataBlock = a + timestamp + "00" + timestamp + b
    dataBlock = binascii.unhexlify(dataBlock)
    newDataBlock = binascii.unhexlify(newDataBlock)
    trpData = open(readPath, "rb").read()
    trpData = trpData.replace(dataBlock, newDataBlock)
    open(readPath, "wb").write(trpData)


def setAccountId(aid):
    a = trpData[:0x120]
    b = trpData[0x120+0x8:]
    newTrpData = a + binascii.unhexlify(aid) + b
    open(readPath, "wb").write(newTrpData)

def unlockTrophy(v):
    if parseTrophyDataBlock(v)["unlocked"] == True:
        return 0
    ParseTRPTITLE.init("data/"+getNpCommId()+"/TRPTITLE.DAT")
    if ParseTRPTITLE.parseDataBlock(v)["unlocked"] == False:
        ParseTRPTITLE.unlockTrophy(v)
    npCommId = getNpCommId()
    ParseTRPSFM.init("conf/"+npCommId+"/TROP.SFM")
    grade = ParseTRPSFM.getAllTrophies()[v]["grade"]
    if grade == "P":
        grade = "01"
    elif grade == "G":
        grade = "02"
    elif grade == "S":
        grade = "03"
    elif grade == "B":
        grade = "04"
    #init(readPath)
    origTrophyDataBlock = getTrophyDataBlock(v)
    trophyDataBlock = origTrophyDataBlock

    a = origTrophyDataBlock[96+2:]
    b = origTrophyDataBlock[:96]
    trophyDataBlock = b + grade + a
    a = trophyDataBlock[32+2:]
    b = trophyDataBlock[:32]
    trophyDataBlock = b + "02" + a
    a = trophyDataBlock[102+2:]
    b = trophyDataBlock[:102]
    trophyDataBlock = b + "20" + a




    trpData = open(readPath, "rb").read()
    trpData = trpData.replace(binascii.unhexlify(origTrophyDataBlock),binascii.unhexlify(trophyDataBlock))
    open(readPath,"wb").write(trpData)
    unlockedTrophys = getNumberOfUnlockedTrophies() + 1
    setNumberOfUnlockedTrophies(unlockedTrophys)



def lockTrophy(v):
    if parseTrophyDataBlock(v)["unlocked"] == True:
        return 0
    origTrophyDataBlock = getTrophyDataBlock(v)
    a = origTrophyDataBlock[96+2:]
    b = origTrophyDataBlock[:96]
    trophyDataBlock = b + "00" + a
    a = trophyDataBlock[32+2:]
    b = trophyDataBlock[:32]
    trophyDataBlock = b + "00" + a
    a = trophyDataBlock[103+2:]
    b = trophyDataBlock[:103]
    trophyDataBlock = b + "00" + a
    trpData = open(readPath, "rb").read()
    trpData = trpData.replace(binascii.unhexlify(origTrophyDataBlock),binascii.unhexlify(trophyDataBlock))
    open(readPath,"wb").write(trpData)
    writeTimestamp(v,"00000000000000")
    init(readPath)
    unlockedTrophys = getNumberOfUnlockedTrophies() - 1
    setNumberOfUnlockedTrophies(unlockedTrophys)


def parseTrophyDataBlock(v):
    trophyDataBlock = getTrophyDataBlock(v)
    trophyType = trophyDataBlock[96:96 + 2]
    if trophyType == "01":
        trophyType = "P"
    elif trophyType == "02":
        trophyType = "G"
    elif trophyType == "03":
        trophyType = "S"
    elif trophyType == "04":
        trophyType = "B"
    else:
        trophyType = "Unknown"
    unlocked = trophyDataBlock[32:32+2]
    if unlocked == "02":
        unlocked = True
    elif unlocked == "00":
        unlocked = False
    else:
        unlocked = "Unknown"
    timestamp = [0,0]
    timestamp[0] = trophyDataBlock[116:116+14]
    timestamp[1] = trophyDataBlock[132:132+14]
    #print {"grade":trophyType,"unlocked":unlocked,"timestamp":timestamp}
    return {"grade":trophyType,"unlocked":unlocked,"timestamp":timestamp}

