#!/usr/bin/env python
# coding=utf-8


numOfGroup = numOfPot = 0
maxLenPot = maxLenConfd = maxLenUEFA = 0
lists = [] # lists of all countries
groups = {} # Dict of each group with assigned countries
pot = {}
confederation = {}
domain = {}
result = ""


def initialcheck():
    global maxLenPot, maxLenConfd, maxLenUEFA ,numOfGroup, result
    maxlen()
    if maxLenPot > numOfGroup:
        result = "No"
    elif maxLenUEFA > 2 * numOfGroup:
        result = "No"
    elif maxLenConfd > numOfGroup:
        result = "No"
    else:
        result = ""


def maxlen():
    global maxLenPot, maxLenConfd, maxLenUEFA
    maxLenPot = max(len(p) for p in pot.values())

    for k, v in confederation.iteritems():
        if k == "UEFA":
            maxLenUEFA = len(v)
        else:
            if maxLenConfd < len(v):
                maxLenConfd = len(v)

def writeout():
    nf = open("output.txt", "w")
    if result == "No":
        nf.write("No")
    elif result == "Yes":
        nf.write("Yes\n")
        countryList = ""
        for k, v in groups.iteritems():
            v.sort()

            if not k == numOfGroup:
                if not len(v) == 0:
                    countryList = ",".join(v) + "\n"
                else:
                    countryList = "None\n"
            else:
                if not len(v) == 0:
                    countryList = ",".join(v)
                else:
                    countryList = "None"

            nf.write(countryList)
    else:
        print "Error!"

    nf.close()


def classify():
    global lists, result
    startAssign()
    if explore(1):
        result = "Yes"
    else:
        result = "No"
    writeout()


def explore(num):
    global lists, groups, numOfGroup
    if len(lists) == 0:
        return True
    else:
        for idx in range(1, numOfGroup + 1):
            if safe(lists[0], idx):
                nextCountry = lists[0]
                lists.remove(nextCountry)
                groups[idx].append(nextCountry)
                if explore(num + 1):
                    return True
                groups[idx].pop()
                lists.insert(0, nextCountry)

    return False


def safe(cun, num):
    global pot, confederation
    idxOfPot = 0
    idxOfConfd = ""
    potList = getPotList(num)
    conList = getConList(num)

    for k1, v1 in pot.iteritems():
        if cun in v1:
            idxOfPot = k1

    for k2, v2 in confederation.iteritems():
        if cun in v2:
            idxOfConfd = k2

    if idxOfPot in potList:
        return False
    elif idxOfConfd in conList:
        if idxOfConfd == "UEFA" and conList.count("UEFA") == 1:
            return True
        else:
            return False
    else:
        return True


def getPotList(num):
    global groups, pot
    lst = []
    for j in range(len(groups[num])):
        country = groups[num][j]
        for k, v in pot.iteritems():
            if country in v:
                lst.append(k)

    return lst


def getConList(num):
    global groups, confederation
    lst = []
    for o in range(len(groups[num])):
        country = groups[num][o]
        for k, v in confederation.iteritems():
            if country in v:
                lst.append(k)
    return lst


def startAssign():
    global groups, domain, lists
    for i in range(1, numOfGroup + 1):
        tmp = []
        groups[i] = tmp

    # Initial domain for each country
    for var in lists:
        dm = [x+1 for x in range(numOfGroup)]
        domain[var] = dm


fp = open("input.txt","r")

numOfGroup = int(fp.readline())
numOfPot = int(fp.readline())

i = 0
for line in fp:
    i += 1
    countries = line.strip("\n\r").split(",")
    pot[i] = countries
    lists.extend(countries)

    if i == numOfPot:
        break

for line in fp:
    tmp = line.split(":")
    key = tmp[0]
    countries = []
    if not tmp[1].strip("\n\r") == "None":
        countries.extend(tmp[1].strip("\n\r").split(","))
    confederation[key] = countries

fp.close()


initialcheck()
if result == "No":
    writeout()
else:
    classify()


