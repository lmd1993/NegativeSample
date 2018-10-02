import glob

"""
1. 3 Gram
2-1. gram gram POS: right to left
2-2. POS gram gram: left to right
3. POS gram POS: left to right
3-1. 2 Gram Left
3-2. 2 Gram Right
4-1. POS gram
4-2. gram POS
8. one gram
9. Other rules: First character's case, 'ed'
10-1. gram_gram
10-2. gram_POS
10-3. POS_gram
10-4. POS_POS
10-5. gram_
10-6. _gram
10-7. POS_
10-8. _POS
11. Use the NNP.... as default if it appears most frequently
May try gram gram gram
"""


def ngrams(s, n=2, i=0):
    while len(s[i:i + n]) == n:
        yield s[i:i + n]
        i += 1


def clean(l):
    removeL = []
    for i in l:
        if i[1] == '-NONE-':
            removeL.append(i)
            input("Press Enter to continue...")
    for i in removeL:
        l.remove(i)
    return l


def cleanAppendBeginningAndEnd(l):
    removeL = []
    for i in l:
        if i[1] == '-NONE-':
            removeL.append(i)
    for i in removeL:
        l.remove(i)
    l.insert(0, ('$$', 'Begin'))
    l.append(('$$$', 'Stop'))
    return l


def ngramRaw(listofNgram):
    temp = ""
    for i in listofNgram:
        temp += i[0]
        temp += " "
    temp = ' '.join(temp.split())
    return temp


def ngramRawGGP(listofNgram, whichPOS):  # gram gram pos
    temp = ""
    which = 0
    for i in listofNgram:
        which += 1
        if which in whichPOS:
            temp += i[1]
        else:
            temp += i[0]
        temp += " "
    temp = ' '.join(temp.split())
    if "|" in temp:  # since we use the | later to split
        temp = temp.replace("|", "&")
    return temp


def ngramRawFor1(listofNgram):
    temp = listofNgram[0]
    return temp


def for1g(listOfTGram):
    dict = {}
    for i in listOfTGram:
        pos2 = i.split("|")[0]
        count = int(i.split("|")[1])
        if pos2 in dict:
            dict[pos2] = dict[pos2] + count
        else:
            dict[pos2] = count
    return max(dict, key=dict.get)


def for2gR(listOfTGram):
    dict = {}
    for i in listOfTGram:
        pos2 = i.split("|")[1]
        count = int(i.split("|")[2])
        if pos2 in dict:
            dict[pos2] = dict[pos2] + count
        else:
            dict[pos2] = count
    return [max(dict, key=dict.get), max(dict.values())]


def for2gL(listOfTGram):
    dict = {}
    for i in listOfTGram:
        pos2 = i.split("|")[0]
        count = int(i.split("|")[2])
        if pos2 in dict:
            dict[pos2] = dict[pos2] + count
        else:
            dict[pos2] = count
    return [max(dict, key=dict.get), max(dict.values())]


def for3g(listOfTGram):
    dict = {}
    for i in listOfTGram:
        pos2 = i.split("|")[1]
        count = int(i.split("|")[3])
        if pos2 in dict:
            dict[pos2] = dict[pos2] + count
        else:
            dict[pos2] = count
    return max(dict, key=dict.get)


def forAnyg(listOfTGram, pos, countPos):
    dict = {}
    for i in listOfTGram:
        pos2 = i.split("|")[pos]
        count = int(i.split("|")[countPos])
        if pos2 in dict:
            dict[pos2] = dict[pos2] + count
        else:
            dict[pos2] = count
    return max(dict, key=dict.get)


def forAnygMore(listOfTGram, pos, countPos):
    dict = {}
    for i in listOfTGram:
        pos2 = i.split("|")[pos]
        count = int(i.split("|")[countPos])
        if pos2 in dict:
            dict[pos2] = dict[pos2] + count
        else:
            dict[pos2] = count
    return [max(dict, key=dict.get), max(dict.values())]


def forAnygMore2(listOfTGramL, posL, listOfTGramR, posR, countPos):
    dict = {}
    for i in listOfTGramL:
        pos2 = i.split("|")[posL]
        count = int(i.split("|")[countPos])
        if pos2 in dict:
            dict[pos2] = dict[pos2] + count
        else:
            dict[pos2] = count
    for i in listOfTGramR:
        pos2 = i.split("|")[posR]
        count = int(i.split("|")[countPos])
        if pos2 in dict:
            dict[pos2] = dict[pos2] + count
        else:
            dict[pos2] = count
    return [max(dict, key=dict.get), max(dict.values())]


def listReplace(l, newStr, oldStr):
    for i, word in enumerate(l):
        if word == oldStr:
            l[i] = newStr
    return l


def update(dictOfngram, ngramT, id, ngr, whichGr):  # key: ngramT; value: id
    if ngramT in dictOfngram[whichGr]:
        listOfTGram = dictOfngram[whichGr][ngramT]
        everMet = False
        for loG in listOfTGram:  # pos1|pos2|pos3|count
            if id in loG:
                newCount = int(loG.split("|")[ngr]) + 1
                id = id + str(newCount)
                listOfTGram = listReplace(listOfTGram, id, loG)
                dictOfngram[whichGr][ngramT] = listOfTGram
                everMet = True
                break
        if not everMet:
            id = id + str(1)
            listOfTGram.append(id)
            dictOfngram[whichGr][ngramT] = listOfTGram
            # print(ngramT)
            # print(listOfTGram)
    else:
        id = id + str(1)
        dictOfngram[whichGr][ngramT] = [id]


def build3Gram(intI, i, j):
    listJ = []
    if intI == 0:  # first word
        listJ.append(('$$', 'Begin'))
        listJ.append(j)
        if intI + 1 < len(i):
    
            listJ.append(i[intI + 1])
    elif intI == len(i) - 1:  # last word
        listJ.append(i[intI - 1])
        listJ.append(j)
        listJ.append(('$$$', 'Stop'))
    else:
        listJ.append(i[intI - 1])
        listJ.append(j)
        listJ.append(i[intI + 1])
    return listJ


def build2Gram(intI, i, j):
    listTwor = []
    listTwol = []
    if intI == 0:  # first word
        listTwor.append(('$$', 'Begin'))
        listTwor.append(j)
    else:
        listTwor.append(i[intI - 1])
        listTwor.append(j)

    if intI == len(i) - 1:  # last word
        listTwol.append(j)
        listTwol.append(('$$$', 'Stop'))
    else:
        listTwol.append(j)
        listTwol.append(i[intI + 1])
    return [listTwor, listTwol]


import nltk
# nltk.download('treebank')
# ngram, pos1+pos2+pos3+count
from nltk.corpus import treebank

nNgram = 3
import pickle

dictOfngram = [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {},
               {}]  # 1, 3 gram; 2, gram gram POS; 3, POS gram gram; 4, POS gram POS; 5, POS gram; 6, gram POS; 7, POS _ POS
# 8, gram _ gram;


import pickle

ii = 0
for i in dictOfngram:
    if ii >= 1:
        with open("regPreDifNoLowerUnderlinePOS/mySavedDictPOS" + str(ii) + ".txt", "rb") as myFile:
            dictOfngram[ii] = pickle.load(myFile)
    ii += 1

dictOfngramMultiple = [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {},
               {}]
ii = 0
for i in dictOfngramMultiple:
    if ii >= 1:
        with open("regPreDifMultipleFeatureNewPOS/mySavedDictPOS" + str(ii) + ".txt", "rb") as myFile:
            dictOfngramMultiple[ii] = pickle.load(myFile)
    ii += 1

# countRight = 0
countInitialRight = 0  # initial going through
count2nd1stRight = 0  # second part first iteration accurate
count2nd2nd = 0  # second part second iteration accurate
count2nd3rd = 0  # second part third iteration accurate
import numpy

totalIteration = 8
countDifGTest = numpy.zeros((19, totalIteration))  # 18 rule for 5 iteration
# countDifGTest[:,0] = ["Test", "3Gram", "GramGramPOS", "PGG", "PGP","GGLeftRight", "PG", "GP", "G", "G_G",
#                       "G_P", "P_G", "P_P", "G_", "_G", "P_","_P","Suffix", "NNP"]
countDifGRight = numpy.zeros((19, totalIteration))
# countDifGRight[:,0] = ["Right", "3Gram", "GramGramPOS", "PGG", "PGP","GGLeftRight", "PG", "GP", "G", "G_G",
#                       "G_P", "P_G", "P_P", "G_", "_G", "P_","_P","Suffix", "NNP"]

totalUpdate = numpy.zeros((19, totalIteration))
totalUpdateToRight = numpy.zeros((19, totalIteration))
totalUpdateToWrong = numpy.zeros((19, totalIteration))
totalIteration -= 1


def ngramRawLineGGP(listofNgram, whichPOS, linePos):  # gram gram pos
    temp = ""
    which = 0
    for i in listofNgram:
        which += 1
        if which in whichPOS:
            temp += i[1]
        elif which == linePos:
            temp += "_"
        else:
            temp += i[0]
        temp += " "
    temp = ' '.join(temp.split())
    if "|" in temp:  # since we use the | later to split
        temp = temp.replace("|", "&")
    return temp

def ngramRawLineGGPMultipleFeature(listofNgram, nsuffix):  # gram gram pos
    temp = ""
    whichPOS = [1, 3]
    which = 0
    for i in listofNgram:
        which += 1
        if which in whichPOS:
            temp += i[1]
        else:
            if i[0][0].isupper():
                temp+="U"
            else:
                temp+="L"
            temp += " "
            if '-' in i[0]:
                temp+="Hyp"
            else:
                temp+="UnH"
            temp += " "
            temp += i[0][-nsuffix:]
        temp += " "
    temp = ' '.join(temp.split())
    if "|" in temp:  # since we use the | later to split
        temp = temp.replace("|", "&")
    return temp


def generateRes(i):
    res = []
    for j in i:
        res.append(tuple((j[0], 'notAssign')))
    return res


def writeContext(j, i, whichGram, iteration, posforj, whichGramR=0, extra="", cpiintI=None, ngramTL="", ngramTR=""):
    """
    f = open("resPOS/" + str(whichGram) + "And" + str(iteration) + "Gram" + extra, "a")
    f.write(ngramRaw(i))
    f.write('\n')
    f.write(j[0])
    f.write(' ')
    f.write(j[1])
    f.write(' ')
    f.write(posforj)
    f.write('\n')
    #print('New')
   # print(whichGram)
    if whichGram < 17:
        if ngramTL in dictOfngram[whichGram]:
            listOfTGramL = dictOfngram[whichGram][ngramTL]
            for i in listOfTGramL:
                # print(i)
                f.write(i)
                f.write(' ')
            f.write('\n')
    whichGramR = int(whichGramR)
    #print(whichGramR)
    if whichGramR < 17:
        if whichGramR > 0:
            if ngramTR in dictOfngram[whichGramR]:
                listOfTGramL = dictOfngram[whichGramR][ngramTR]
                for i in listOfTGramL:
                    # print(i)
                    f.write(i)
                    f.write(' ')
                f.write('\n')
    if cpiintI != None:
        f.write('Pre ')
        f.write(cpiintI[1])
        f.write('\n')
    f.close()
    """
    return 1
    # print("")

def ruleAndResult(listJ, ngramT2, dic, j, countInitialRight, countDifGTest, countDifGRight, totalUpdate,
                  totalUpdateToRight, totalUpdateToWrong, whichGram, pos, countPos, intI, iteration, i):
    if 'notAssign' in ngramT2:
        return False  # contain not assigned pos tag
    #if 'UnH' in ngramT2:
     #   print("")
    if17 = False
    if whichGram == 17:
        if17 = True
        whichGram = 9
    if ngramT2 in dic[whichGram]:
        #print("in the")
        listOfTGram = []
        if not if17:
            listOfTGram = dic[whichGram][ngramT2]
        if if17:
            listOfTGram = dic[9][ngramT2]
            whichGram = 17
        posforj = forAnyg(listOfTGram, pos, countPos)
        if cpI[intI][1] != posforj:
            totalUpdate[whichGram][iteration] = totalUpdate[whichGram][iteration] + 1
            if posforj == j[1]:
                totalUpdateToRight[whichGram][iteration] += 1
                writeContext(j, i, whichGram, iteration, posforj, extra="updateToRight", cpiintI=cpI[intI])
            elif cpI[intI][1] == j[1]:
                totalUpdateToWrong[whichGram][iteration] += 1
                writeContext(j, i, whichGram, iteration, posforj, extra="updateToNotRight", cpiintI=cpI[intI])
        cpI[intI] = tuple((j[0], posforj))
        countDifGTest[whichGram][iteration] = countDifGTest[whichGram][iteration] + 1

        if posforj == j[1]:
            countInitialRight += 1
            countDifGRight[whichGram][iteration] += 1
        elif posforj != "":
            writeContext(j, i, whichGram, iteration, posforj, ngramTL=ngramT2)
        return True
    else:
        #print("not in")
        return False


def ruleMoreAndResult(ngramT2, dictOfngram, whichGram, pos, countPos):
    if 'notAssign' in ngramT2:
        return None  # contain not assigned pos tag
    if ngramT2 in dictOfngram[whichGram]:
        listOfTGram = dictOfngram[whichGram][ngramT2]
        [posforj, r] = forAnygMore(listOfTGram, pos, countPos)
        countR = 0
        for loG in listOfTGram:
            countR += int(loG.split("|")[countPos])

        return [countR, r, posforj]
    return None


# ngramTL, ngramTR, dictOfngram, whichGramL, whichGramR, posL, posR, countPos, iteration, countInitialRight
def ruleMoreAndResultMore(listJ, ngramTL, ngramTR, dictOfngram, j, countInitialRight, countDifGTest, countDifGRight,
                          totalUpdate, totalUpdateToRight, totalUpdateToWrong, whichGramL, whichGramR, posL, posR,
                          countPos, intI, iteration, i):
    listofGramL = []
    listofGramR = []
    if ngramTL in dictOfngram[whichGramL]:
        listofGramL = dictOfngram[whichGramL][ngramTL]
    if ngramTR in dictOfngram[whichGramR]:
        listofGramR = dictOfngram[whichGramR][ngramTR]
    posforj = ""
    if len(listofGramR) > 0 or len(listofGramL) > 0:
        [posforj, r] = forAnygMore2(listofGramL, posL, listofGramR, posR, countPos)

    countR = 0
    for loG in listofGramL:
        countR += int(loG.split("|")[countPos])
    for loG in listofGramR:
        countR += int(loG.split("|")[countPos])
    if countR < 1:
        return False
    whichGram = whichGramL
    if cpI[intI][1] != posforj:
        totalUpdate[whichGram][iteration] = totalUpdate[whichGram][iteration] + 1
        if posforj == j[1]:
            totalUpdateToRight[whichGram][iteration] += 1
            writeContext(j, i, whichGram, iteration, posforj, whichGramR, extra="updateToRight", cpiintI=cpI[intI])
        elif cpI[intI][1] == j[1]:
            totalUpdateToWrong[whichGram][iteration] += 1
            writeContext(j, i, whichGram, iteration, posforj, whichGramR, extra="updateToNotRight", cpiintI=cpI[intI])
    cpI[intI] = tuple((j[0], posforj))
    countDifGTest[whichGram][iteration] = countDifGTest[whichGram][iteration] + 1

    if posforj == j[1]:
        countInitialRight += 1
        countDifGRight[whichGram][iteration] += 1
    elif posforj != "":
        writeContext(j, i, whichGram, iteration, posforj, whichGramR, ngramTL=ngramTL, ngramTR=ngramTR)
    return True


# ngramTL: left ngram text
# ngramTR: right ngram text
# dictOfngram: dictionary
# j: the target word
# countInitialRight: Right condition
# countDifGTest: different test condition
# countDifGRight: diffrent rule right
# totalUpdate: total update
# totalUpdateToRight: update to right
# totalUpdateToWrong: update to wrong
# whichGramL: left side use
# whichGramR: right side use
# posL: where is the left pos(word)
# posR: where is the right pos(word)
# countPos: where is count
# intI: the id of the word
# iteration: the iteration
# i: context

def multipleRuleAndResult(listJ, ngramTL, ngramTR, dictOfngram, j, countInitialRight, countDifGTest, countDifGRight,
                          totalUpdate, totalUpdateToRight, totalUpdateToWrong, whichGramL, whichGramR, posL, posR,
                          countPos, intI, iteration, i):
    countL = 0
    l = 0
    posOnL = ""
    countR = 0
    r = 0
    posOnR = ""
    posforj = ""
    if ngramTL in dictOfngram[whichGramL]:
        res = ruleMoreAndResult(ngramTL, dictOfngram, whichGramL, posL, countPos)
        if res != None:
            [countL, l, posOnL] = res

    if ngramTR in dictOfngram[whichGramR]:
        res = ruleMoreAndResult(ngramTR, dictOfngram, whichGramR, posR, countPos)
        if res != None:
            [countR, r, posOnR] = res
    rL = 0
    rR = 0
    if countL > 0: rL = l / float(countL)
    if countR > 0: rR = r / float(countR)
    chooseL = False
    chooseR = False
    if countL == 0 and countR > 0:
        posforj = posOnR
        chooseR = True
    elif countL > 0 and countR == 0:
        posforj = posOnL
        chooseL = True
    elif countL == 0 and countR == 0:
        # one gram
        return False
    elif (countL < 3 and countR < 3):
        if rL > rR:
            posforj = posOnL
            chooseL = True
        else:
            posforj = posOnR
            chooseR = True
    elif countL >= 3 and countR < 3:
        posforj = posOnL
        chooseL = True
    elif countL < 3 and countR >= 3:
        posforj = posOnR
        chooseR = True
    elif countL >= 3 and countR >= 3:
        if rL > rR:
            posforj = posOnL
            chooseL = True
        else:
            posforj = posOnR
            chooseR = True
    whichGram = 0
    if chooseL:  # choose Left finally
        whichGram = whichGramL
    if chooseR:  # choose Right finally
        whichGram = whichGramR
    if cpI[intI][1] != posforj:
        totalUpdate[whichGram][iteration] = totalUpdate[whichGram][iteration] + 1
        if posforj == j[1]:
            totalUpdateToRight[whichGram][iteration] += 1
            writeContext(j, i, whichGram, iteration, posforj, "updateToRight", cpiintI=cpI[intI])
        elif cpI[intI][1] == j[1]:
            totalUpdateToWrong[whichGram][iteration] += 1
            writeContext(j, i, whichGram, iteration, posforj, extra="updateToNotRight", cpiintI=cpI[intI])

    cpI[intI] = tuple((j[0], posforj))
    countDifGTest[whichGram][iteration] = countDifGTest[whichGram][iteration] + 1

    if posforj == j[1]:
        countInitialRight += 1
        countDifGRight[whichGram][iteration] += 1
    elif posforj != "":
        writeContext(j, i, whichGram, iteration, posforj)

    return True

# a = ["%.2d" % i for i in range(22, 25)]
oneWordSum = 0
oneWordRight = 0
wordNum = 0
with open("convertedStanfordTagTestEnglish2", "r") as ins:
    for line in ins:
        checkR = []
        if line != '\n':
            oneword = False
            line = line.replace(' \n', '')
            #print(line)
            linArr = line.split(' ')
            wordNum = wordNum + len(linArr)
            for j in linArr:
                if '_' in j:
                    checkR.append((j.split('_')[0], j.split('_')[1]))

# for aa in a:
#     # lis = ["/Users/MingdaLi/PycharmProjects/nec/TREEBANK_3/MRG/WSJ/19/WSJ_1996.MRG"]
#     lis = glob.glob("/Users/MingdaLi/PycharmProjects/nec/TREEBANK_3/MRG/WSJ/"+str(aa)+"/*.MRG")
#     # lis = glob.glob("/home/lmd1993/TREEBANK_3/MRG/WSJ/" + str(aa) + "/*.MRG")
#     for lisStr in lis:
#         print(lisStr)
#         checkR = treebank.tagged_sents(lisStr)
            i = checkR
            i = clean(i)
            cpI = generateRes(i)
            if len(i) <= 1:
                oneword = True

            intI = 0
            # 1st pas One gram +suffix+ other rules + NNP
            # BL: One gram + suffix
            whichGram = 8
            for j in i:
                if 'notAssign' in cpI[intI]:
                    posforj = ""
                    j0 = ngramRawFor1(j)
                    if j0 in dictOfngram[whichGram]:
                        listOfTGram = dictOfngram[whichGram][j0]
                        posforj = for1g(listOfTGram)
                        cpI[intI] = tuple((j[0], posforj))
                        countDifGTest[whichGram][0] = countDifGTest[whichGram][0] + 1  # 1 is the normal 3 gram
                        if posforj == j[1]:
                            if oneword:
                                oneWordRight = oneWordRight + 1
                            countInitialRight += 1
                            countDifGRight[whichGram][0] = countDifGRight[whichGram][0] + 1
                        elif posforj != "":
                            writeContext(j, i, whichGram, 0, posforj, ngramTL=j0)
                intI += 1
            intI = 0
            # suffix
            whichGram = 17
            for j in i:
                if 'notAssign' in cpI[intI]:
                    posforj = ""
                    j0 = ngramRawFor1(j)
                    import re

                    pattern = re.compile(r'(^[-+]?([0-9]+)([.,][0-9]+)?)$')
                    if pattern.fullmatch(j0) != None:
                        posforj = 'NUM'
                    else:
                        rgx = re.compile(r'\d.*?[A-Z].*?[a-z]')
                        if j0[0].isupper():
                            posforj = 'PROPN'
                        elif (j0[-2:] == 'ed' or j0[-3:] == 'ing') and ('-' in j0):
                            posforj = 'ADJ'
                        elif (j0[-2:] == 'ed') and ('-' not in j0):
                            posforj = 'VERB'
                        elif (j0[-3:] == 'ing') and ('-' not in j0):
                            posforj = 'VERB'
                        elif (j0[-2:] == 'er' or j0[-2:] == 'or' or j0[-4:] == 'tion' or j0[-3:] == 'ism' or j0[
                                                                                                             -4:] == 'ment'):
                            posforj = 'NOUN'
                        elif (j0[-3:] == 'ers' or j0[-3:] == 'ors' or j0[-5:] == 'tions' or j0[-4:] == 'isms' or j0[
                                                                                                                 -5:] == 'ments'):
                            posforj = 'NOUN'
                        elif ('-' in j0 or j0[:2] == 'un' or j0[-2:] == 'al' or j0[-3:] == 'ous' or j0[
                                                                                                    -3:] == 'ful' or j0[
                                                                                                                     -4:] == 'able' or j0[
                                                                                                                                       -4:] == 'ible' or j0[
                                                                                                                                                         -3:] == 'ous' or j0[
                                                                                                                                                                          -2:] == 'ic'):
                            posforj = 'ADJ'
                        elif (j0[-2:] == 'ly'):
                            posforj = 'ADV'
                        elif (j0[-1:] == 's'):
                            posforj = 'NOUN'
                        else:
                            # if just a word, we will make decision
                            if oneword:
                                posforj = 'NOUN'
                    if posforj != "":  # we have applied the suffix rule
                        cpI[intI] = tuple((j[0], posforj))
                        countDifGTest[whichGram][0] = countDifGTest[whichGram][0] + 1  # 1 is the normal 3 gram
                    if posforj == j[1]:
                        if oneword:
                            oneWordRight = oneWordRight + 1
                        countInitialRight += 1
                        countDifGRight[whichGram][0] = countDifGRight[whichGram][0] + 1
                    elif posforj != "":
                        writeContext(j, i, whichGram, 0, posforj)
                intI += 1

            if oneword:
                oneWordSum = oneWordSum + 1
                continue

            # BW: other rules
            intI = 0
            while intI < len(i):  # scan right to the left
                j = i[intI]
                # for gram_gram, gram_p, p_g, p_p, g_, _g, p_, _p
                if 'notAssign' in cpI[intI]:  # not covered by previous gram
                    listJ = build3Gram(intI, cpI, j=cpI[intI])  # build the 3 Gram with the cpI
                    ngramT = ngramRawLineGGP(listJ, [], 2)  # gram_gram
                    whichGram = 9
                    if not ruleAndResult(listJ, ngramT, dictOfngram, j, countInitialRight, countDifGTest,
                                         countDifGRight, totalUpdate, totalUpdateToRight, totalUpdateToWrong, whichGram,
                                         pos=1, countPos=3, intI=intI, iteration=0, i=i):
                        ngramTR = ngramRawLineGGP(listJ, [3], 2)  # gram_pos
                        whichGramR = 10
                        ngramTL = ngramRawLineGGP(listJ, [1], 2)  # pos_gram
                        whichGramL = 11
                        posL = 1
                        posR = 1
                        if not ruleMoreAndResultMore(listJ, ngramTL, ngramTR, dictOfngram, j, countInitialRight,
                                                     countDifGTest, countDifGRight, totalUpdate, totalUpdateToRight,
                                                     totalUpdateToWrong, whichGramL, whichGramR, posL, posR,
                                                     countPos=3, intI=intI, iteration=0, i=i):
                            ngramT = ngramRawLineGGP(listJ, [1, 3], 2)  # pos_pos
                            whichGram = 12
                            if not ruleAndResult(listJ, ngramT, dictOfngram, j, countInitialRight, countDifGTest,
                                                 countDifGRight, totalUpdate, totalUpdateToRight, totalUpdateToWrong,
                                                 whichGram, pos=1, countPos=3, intI=intI,
                                                 iteration=0, i=i):
                                [listTwor, listTwol] = build2Gram(intI, i, j=i[intI])  # get two gram
                                ngramT = ngramRawLineGGP(listTwor, [],
                                                         2)  # gram_  whichUsePOS, linePosition, start from 1
                                whichGram = 13
                                if not ruleAndResult(listJ, ngramT, dictOfngram, j, countInitialRight,
                                                     countDifGTest,
                                                     countDifGRight, totalUpdate, totalUpdateToRight,
                                                     totalUpdateToWrong, whichGram, pos=1, countPos=2, intI=intI,
                                                     iteration=0,
                                                     i=i):  # countPos and pos is different from the others start from 0, pos is the position of the target word, start from 0
                                    ngramT = ngramRawLineGGP(listTwol, [],
                                                             1)  # _gram whichUsePOS, linePosition, start from 1
                                    whichGram = 14
                                    if not ruleAndResult(listJ, ngramT, dictOfngram, j, countInitialRight,
                                                         countDifGTest,
                                                         countDifGRight, totalUpdate, totalUpdateToRight,
                                                         totalUpdateToWrong, whichGram, pos=0, countPos=2, intI=intI,
                                                         iteration=0,
                                                         i=i):  # pos: position of target word; countPos: the count attribute 's  position
                                        ngramT = ngramRawLineGGP(listTwor, [1],
                                                                 2)  # pos_, whichUsePOS, linePosition, start from 1
                                        whichGram = 15
                                        if not ruleAndResult(listJ, ngramT, dictOfngram, j, countInitialRight,
                                                             countDifGTest,
                                                             countDifGRight, totalUpdate, totalUpdateToRight,
                                                             totalUpdateToWrong, whichGram, pos=1, countPos=2,
                                                             intI=intI,
                                                             iteration=0,
                                                             i=i):  # pos: position of target word; countPos: the count attribute 's  position start from 0
                                            ngramT = ngramRawLineGGP(listTwol, [2],
                                                                     1)  # a_pos, whichUsePOS, linePosition, start from 1
                                            whichGram = 16
                                            if not ruleAndResult(listJ, ngramT, dictOfngram, j, countInitialRight,
                                                                 countDifGTest,
                                                                 countDifGRight, totalUpdate, totalUpdateToRight,
                                                                 totalUpdateToWrong, whichGram, pos=0, countPos=2,
                                                                 intI=intI,
                                                                 iteration=0,
                                                                 i=i):  # pos: position of target word; countPos: the count attribute 's  position start from 0
                                                # use NNP
                                                posforj = "NOUN"
                                                whichGram = 18
                                                cpI[intI] = tuple((j[0], posforj))
                                                countDifGTest[whichGram][0] = countDifGTest[whichGram][
                                                                                  0] + 1
                                                if posforj == j[1]:
                                                    countInitialRight += 1
                                                    countDifGRight[whichGram][0] += 1
                                                elif posforj != "":
                                                    writeContext(j, i, whichGram, 0, posforj)

                intI += 1
            # BW: 3 iterations for all the rules by word


            for iter in range(1, totalIteration):
                intI = 0
                while intI < len(i):  # scan right to the left
                    j = i[intI]
                    cannotSolve = False
                    # for gram_gram, gram_p, p_g, p_p, g_, _g, p_, _p
                    listJ = build3Gram(intI, cpI, j=cpI[intI])  # build the 3 Gram with the cpI
                    ngramT = ngramRawLineGGP(listJ, [], 0)  # gramgramgram
                    whichGram = 1
                    if not ruleAndResult(listJ, ngramT, dictOfngramMultiple, j, countInitialRight, countDifGTest,
                                         countDifGRight, totalUpdate, totalUpdateToRight, totalUpdateToWrong, whichGram,
                                         pos=1, countPos=3, intI=intI, iteration=iter, i=i):
                        # gramgrampos Compare posgramgram
                        ngramTR = ngramRawLineGGP(listJ, [3], 0)  # gramgrampos
                        ngramTL = ngramRawLineGGP(listJ, [1], 0)  # posgramgram
                        whichGramR = 2  # gramgrampos
                        whichGramL = 3  # posgramgram
                        posR = 1
                        posL = 1
                        if not ruleMoreAndResultMore(listJ, ngramTL, ngramTR, dictOfngramMultiple, j, countInitialRight,
                                                     countDifGTest, countDifGRight, totalUpdate, totalUpdateToRight,
                                                     totalUpdateToWrong, whichGramL, whichGramR, posL, posR, countPos=3,
                                                     intI=intI, iteration=iter, i=i):
                            ngramT = ngramRawLineGGP(listJ, [1, 3], 0)  # posgrampos
                            whichGram = 4
                            if not ruleAndResult(listJ, ngramT, dictOfngramMultiple, j, countInitialRight,
                                                 countDifGTest,
                                                 countDifGRight, totalUpdate, totalUpdateToRight, totalUpdateToWrong,
                                                 whichGram, pos=1, countPos=3, intI=intI,
                                                 iteration=iter, i=i):
                                [listTwor, listTwol] = build2Gram(intI, i, j=i[intI])  # get two gram
                                ngramTR = ngramRawLineGGP(listTwor, [],
                                                          0)  # gramgram  whichUsePOS, linePosition, start from 1
                                ngramTL = ngramRawLineGGP(listTwol, [],
                                                          0)  # gramgram whichUsePOS, linePosition, start from 1
                                whichGramR = 5
                                whichGramL = 5
                                posR = 1
                                posL = 0
                                if not ruleMoreAndResultMore(listJ, ngramTL, ngramTR, dictOfngramMultiple, j, countInitialRight,
                                                             countDifGTest, countDifGRight, totalUpdate,
                                                             totalUpdateToRight, totalUpdateToWrong, whichGramL,
                                                             whichGramR, posL, posR, countPos=2, intI=intI,
                                                             iteration=iter, i=i):

                                    ngramTL = ngramRawLineGGP(listTwor, [1],
                                                              0)  # posgram, whichUsePOS, linePosition, start from 1
                                    whichGramL = 6
                                    ngramTR = ngramRawLineGGP(listTwol, [2],
                                                              0)  # agrampos, whichUsePOS, linePosition, start from 1
                                    whichGramR = 7

                                    posL = 1
                                    posR = 0
                                    if not ruleMoreAndResultMore(listJ, ngramTL, ngramTR, dictOfngramMultiple, j,
                                                                 countInitialRight, countDifGTest,
                                                                 countDifGRight, totalUpdate,
                                                                 totalUpdateToRight, totalUpdateToWrong,
                                                                 whichGramL, whichGramR, posL, posR, countPos=2,
                                                                 intI=intI, iteration=iter, i=i):
                                        # New: First see if all number then CD. Then see the matching.
                                        # If all number
                                        j0 = ngramRawFor1(j)
                                        whichGram = 14
                                        posforj = ""
                                        import re
                                        pattern = re.compile(r'(^[-+]?([0-9]+)(\.[0-9]+)?)$')
                                        if pattern.fullmatch(j0) != None or pattern.fullmatch(
                                                j0.replace(",", "")) != None:
                                            posforj = 'NUM'
                                            if cpI[intI][1] != posforj:
                                                totalUpdate[whichGram][iter] = totalUpdate[whichGram][
                                                                               iter] + 1
                                                if posforj == j[1]:
                                                    totalUpdateToRight[whichGram][iter] += 1
                                                    writeContext(j, i, whichGram, iter, posforj,
                                                                 extra="updateToRight", cpiintI=cpI[intI])
                                                elif cpI[intI][1] == j[1]:
                                                    totalUpdateToWrong[whichGram][iter] += 1
                                                    writeContext(j, i, whichGram, iter, posforj,
                                                                 extra="updateToNotRight", cpiintI=cpI[intI])
                                            cpI[intI] = tuple((j[0], posforj))
                                            countDifGTest[whichGram][iter] = countDifGTest[whichGram][
                                                                                 iter] + 1  # 1 is the normal 3 gram
                                            if posforj == j[1]:
                                                countInitialRight += 1
                                                countDifGRight[whichGram][iter] = countDifGRight[whichGram][iter] + 1
                                            elif posforj != "":
                                                writeContext(j, i, whichGram, iter, posforj)
                                        else:
                                            # suffix Other rules
                                            listJ = build3Gram(intI, cpI, j=cpI[intI])  # build the 3 Gram with the cpI
                                            ngramT = ngramRawLineGGPMultipleFeature(listJ, 5)  # 5 suf
                                            whichGram = 8
                                            if not ruleAndResult(listJ, ngramT, dictOfngramMultiple, j,
                                                                 countInitialRight,
                                                                 countDifGTest,
                                                                 countDifGRight, totalUpdate, totalUpdateToRight,
                                                                 totalUpdateToWrong, whichGram,
                                                                 pos=1, countPos=3, intI=intI, iteration=iter,
                                                                 i=i):
                                                # countPos and pos is different from the others start from 0
                                                # , pos is the position of the target word, start from 0
                                                listJ = build3Gram(intI, cpI,
                                                                   j=cpI[intI])  # build the 3 Gram with the cpI
                                                ngramT = ngramRawLineGGPMultipleFeature(listJ, 4)  # 4 suf
                                                whichGram = 9
                                                if not ruleAndResult(listJ, ngramT, dictOfngramMultiple, j,
                                                                     countInitialRight,
                                                                     countDifGTest,
                                                                     countDifGRight, totalUpdate, totalUpdateToRight,
                                                                     totalUpdateToWrong, whichGram,
                                                                     pos=1, countPos=3, intI=intI, iteration=iter,
                                                                     i=i):  # countPos and pos is different from the others start from 0, pos is the

                                                    listJ = build3Gram(intI, cpI, j=cpI[intI])  # build the 3 Gram with the cpI
                                                    ngramT = ngramRawLineGGPMultipleFeature(listJ, 3)  # 3 suf
                                                    whichGram = 10
                                                    cannotSolve = False
                                                    if not ruleAndResult(listJ, ngramT, dictOfngramMultiple, j, countInitialRight,
                                                                         countDifGTest,
                                                                         countDifGRight, totalUpdate, totalUpdateToRight,
                                                                         totalUpdateToWrong, whichGram,
                                                                         pos=1, countPos=3, intI=intI, iteration=iter, i=i): # countPos and pos is different from the others start from 0, pos is the position of the target word, start from 0




                                                        # 1 Gram
                                                        j0 = ngramRawFor1(j)  # one gram
                                                        whichGram = 15 # to get from the list
                                                        posforj = ""
                                                        if j0 in dictOfngram[8]:
                                                            listOfTGram = dictOfngram[8][j0]
                                                            posforj = for1g(listOfTGram)
                                                            if cpI[intI][1] != posforj:
                                                                totalUpdate[whichGram][iter] = totalUpdate[whichGram][
                                                                                                   iter] + 1
                                                                if posforj == j[1]:
                                                                    totalUpdateToRight[whichGram][iter] += 1
                                                                    writeContext(j, i, whichGram, iter, posforj,
                                                                                 extra="updateToRight", cpiintI=cpI[intI])
                                                                elif cpI[intI][1] == j[1]:
                                                                    totalUpdateToWrong[whichGram][iter] += 1
                                                                    writeContext(j, i, whichGram, iter, posforj,
                                                                                 extra="updateToNotRight", cpiintI=cpI[intI])
                                                            cpI[intI] = tuple((j[0], posforj))
                                                            countDifGTest[whichGram][iter] = countDifGTest[whichGram][
                                                                                                 iter] + 1  # 1 is the normal 3 gram
                                                            if posforj == j[1]:
                                                                countInitialRight += 1
                                                                countDifGRight[whichGram][iter] = countDifGRight[whichGram][
                                                                                                      iter] + 1
                                                            elif posforj != "":
                                                                writeContext(j, i, whichGram, iter, posforj, ngramTL=j0)
                                                        else:
                                                            whichGram = 16
                                                            rgx = re.compile(r'\d.*?[A-Z].*?[a-z]')
                                                            if j0[0].isupper():
                                                                posforj = 'PROPN'
                                                            elif (j0[-2:] == 'ed' or j0[-3:] == 'ing') and ('-' in j0):
                                                                posforj = 'ADJ'
                                                            elif (j0[-2:] == 'ed') and ('-' not in j0):
                                                                posforj = 'VERB'
                                                            elif (j0[-3:] == 'ing') and ('-' not in j0):
                                                                posforj = 'VERB'
                                                            elif (j0[-2:] == 'er' or j0[-2:] == 'or' or j0[
                                                                                                        -4:] == 'tion' or j0[
                                                                                                                          -3:] == 'ism' or j0[
                                                                                                                                           -4:] == 'ment'):
                                                                posforj = 'NOUN'
                                                            elif (j0[-3:] == 'ers' or j0[-3:] == 'ors' or j0[
                                                                                                          -5:] == 'tions' or j0[
                                                                                                                             -4:] == 'isms' or j0[
                                                                                                                                               -5:] == 'ments'):
                                                                posforj = 'NOUN'
                                                            elif ('-' in j0 or j0[:2] == 'un' or j0[-2:] == 'al' or j0[
                                                                                                                    -3:] == 'ous' or j0[
                                                                                                                                     -3:] == 'ful' or j0[
                                                                                                                                                      -4:] == 'able' or j0[
                                                                                                                                                                        -4:] == 'ible' or j0[
                                                                                                                                                                                          -3:] == 'ous' or j0[
                                                                                                                                                                                                           -2:] == 'ic'):
                                                                posforj = 'ADJ'
                                                            elif (j0[-2:] == 'ly'):
                                                                posforj = 'ADV'
                                                            elif (j0[-1:] == 's'):
                                                                posforj = 'NOUN'
                                                            #if posforj != j[1]:
                                                             #   print(j[0])
                                                              #  print(j[1])
                                                               # print(posforj)
                                                            if posforj != "":  # we have applied the suffix rule
                                                                if cpI[intI][1] != posforj:
                                                                    totalUpdate[whichGram][iter] = totalUpdate[whichGram][
                                                                                                       iter] + 1
                                                                    if posforj == j[1]:
                                                                        totalUpdateToRight[whichGram][iter] += 1
                                                                        writeContext(j, i, whichGram, iter, posforj,
                                                                                     extra="updateToRight", cpiintI=cpI[intI])
                                                                    elif cpI[intI][1] == j[1]:
                                                                        totalUpdateToWrong[whichGram][iter] += 1
                                                                        writeContext(j, i, whichGram, iter, posforj,
                                                                                     extra="updateToNotRight",
                                                                                     cpiintI=cpI[intI])
                                                                cpI[intI] = tuple((j[0], posforj))
                                                                countDifGTest[whichGram][iter] = countDifGTest[whichGram][
                                                                                                     iter] + 1  # 1 is the normal 3 gram
                                                            if posforj == j[1]:
                                                                countInitialRight += 1
                                                                countDifGRight[whichGram][iter] = countDifGRight[whichGram][
                                                                                                      iter] + 1
                                                            elif posforj != "":
                                                                writeContext(j, i, whichGram, iter, posforj)
                                                            if posforj == "":
                                                                cannotSolve = True

                                                        if cannotSolve:
                                                            ngramT = ngramRawLineGGPMultipleFeature(listJ, 2)  # 2 suf
                                                            #print(ngramT + ",")
                                                            whichGram = 11
                                                            if not ruleAndResult(listJ, ngramT, dictOfngramMultiple, j, countInitialRight,
                                                                                 countDifGTest,
                                                                                 countDifGRight, totalUpdate, totalUpdateToRight,
                                                                                 totalUpdateToWrong, whichGram,
                                                                                 pos=1, countPos=3, intI=intI, iteration=iter, i=i):
                                                                ngramT = ngramRawLineGGPMultipleFeature(listJ, 1)  # 1 suf
                                                                #print(ngramT + ",")
                                                                whichGram = 12
                                                                if not ruleAndResult(listJ, ngramT, dictOfngramMultiple, j,
                                                                                     countInitialRight,
                                                                                     countDifGTest,
                                                                                     countDifGRight, totalUpdate,
                                                                                     totalUpdateToRight,
                                                                                     totalUpdateToWrong, whichGram,
                                                                                     pos=1, countPos=3, intI=intI, iteration=iter,
                                                                                     i=i):

                                                                    # G_G
                                                                    listJ = build3Gram(intI, cpI, j=cpI[
                                                                        intI])  # build the 3 Gram with the cpI
                                                                    ngramT = ngramRawLineGGP(listJ, [], 2)  # gram_gram
                                                                    whichGram = 17
                                                                    if not ruleAndResult(listJ, ngramT, dictOfngram, j,
                                                                                         countInitialRight, countDifGTest,
                                                                                         countDifGRight, totalUpdate,
                                                                                         totalUpdateToRight, totalUpdateToWrong,
                                                                                         whichGram, pos=1, countPos=3,
                                                                                         intI=intI, iteration=iter, i=i):

                                                                        posforj = "NOUN"
                                                                        whichGram = 13
                                                                        if cpI[intI][1] != posforj:
                                                                            totalUpdate[whichGram][iter] = totalUpdate[whichGram][
                                                                                                               iter] + 1
                                                                            if posforj == j[1]:
                                                                                totalUpdateToRight[whichGram][iter] += 1
                                                                                writeContext(j, i, whichGram, iter, posforj,
                                                                                             extra="updateToRight", cpiintI=cpI[intI])
                                                                            elif cpI[intI][1] == j[1]:
                                                                                totalUpdateToWrong[whichGram][iter] += 1
                                                                                writeContext(j, i, whichGram, iter, posforj,
                                                                                             extra="updateToNotRight",
                                                                                             cpiintI=cpI[intI])
                                                                        cpI[intI] = tuple((j[0], posforj))
                                                                        countDifGTest[whichGram][iter] = countDifGTest[whichGram][
                                                                                                          iter] + 1
                                                                        if posforj == j[1]:
                                                                            countInitialRight += 1
                                                                            countDifGRight[whichGram][iter] += 1
                                                                        elif posforj != "":
                                                                            writeContext(j, i, whichGram, iter, posforj)


                    intI += 1
"""
                                                # pos: position of target word; countPos: the count attribute 's  position start from 0
                                        j0 = ngramRawFor1(j)  # one gram
                                        whichGram = 8
                                        posforj = ""
                                        if j0 in dictOfngram[whichGram]:
                                            listOfTGram = dictOfngram[whichGram][j0]
                                            posforj = for1g(listOfTGram)
                                            if cpI[intI][1] != posforj:
                                                totalUpdate[whichGram][iter] = totalUpdate[whichGram][
                                                                                   iter] + 1
                                                if posforj == j[1]:
                                                    totalUpdateToRight[whichGram][iter] += 1
                                                    writeContext(j, i, whichGram, iter, posforj,
                                                                 extra="updateToRight", cpiintI=cpI[intI])
                                                elif cpI[intI][1] == j[1]:
                                                    totalUpdateToWrong[whichGram][iter] += 1
                                                    writeContext(j, i, whichGram, iter, posforj,
                                                                 extra="updateToNotRight", cpiintI=cpI[intI])
                                            cpI[intI] = tuple((j[0], posforj))
                                            countDifGTest[whichGram][iter] = countDifGTest[whichGram][
                                                                                 iter] + 1  # 1 is the normal 3 gram
                                            if posforj == j[1]:
                                                countInitialRight += 1
                                                countDifGRight[whichGram][iter] = countDifGRight[whichGram][iter] + 1
                                            elif posforj != "":
                                                writeContext(j, i, whichGram, iter, posforj, ngramTL=j0)
                                        else:
                                            whichGram = 17
                                            pattern = re.compile(r'(^[-+]?([0-9]+)(\.[0-9]+)?)$')
                                            if pattern.fullmatch(j0) != None or pattern.fullmatch(
                                                    j0.replace(",", "")) != None:
                                                posforj = 'CD'
                                            else:
                                                rgx = re.compile(r'\d.*?[A-Z].*?[a-z]')
                                                if j0[0].isupper():
                                                    posforj = 'NNP'
                                                elif (j0[-2:] == 'ed' or j0[-3:] == 'ing') and ('-' in j0):
                                                    posforj = 'JJ'
                                                elif (j0[-2:] == 'ed') and ('-' not in j0):
                                                    posforj = 'VBN'
                                                elif (j0[-3:] == 'ing') and ('-' not in j0):
                                                    posforj = 'VBG'
                                                elif (j0[-2:] == 'er' or j0[-2:] == 'or' or j0[
                                                                                            -4:] == 'tion' or j0[
                                                                                                              -3:] == 'ism' or j0[
                                                                                                                               -4:] == 'ment'):
                                                    posforj = 'NN'
                                                elif (j0[-3:] == 'ers' or j0[-3:] == 'ors' or j0[
                                                                                              -5:] == 'tions' or j0[
                                                                                                                 -4:] == 'isms' or j0[
                                                                                                                                   -5:] == 'ments'):
                                                    posforj = 'NNS'
                                                elif ('-' in j0 or j0[:2] == 'un' or j0[-2:] == 'al' or j0[
                                                                                                        -3:] == 'ous' or j0[
                                                                                                                         -3:] == 'ful' or j0[
                                                                                                                                          -4:] == 'able' or j0[
                                                                                                                                                            -4:] == 'ible' or j0[
                                                                                                                                                                              -3:] == 'ous' or j0[
                                                                                                                                                                                               -2:] == 'ic'):
                                                    posforj = 'JJ'
                                                elif (j0[-2:] == 'ly'):
                                                    posforj = 'BR'
                                                elif (j0[-1:] == 's'):
                                                    posforj = 'NNS'
                                            if posforj != j[1]:
                                                print(j[0])
                                                print(j[1])
                                                print(posforj)
                                            if posforj != "":  # we have applied the suffix rule
                                                if cpI[intI][1] != posforj:
                                                    totalUpdate[whichGram][iter] = totalUpdate[whichGram][
                                                                                       iter] + 1
                                                    if posforj == j[1]:
                                                        totalUpdateToRight[whichGram][iter] += 1
                                                        writeContext(j, i, whichGram, iter, posforj,
                                                                     extra="updateToRight", cpiintI=cpI[intI])
                                                    elif cpI[intI][1] == j[1]:
                                                        totalUpdateToWrong[whichGram][iter] += 1
                                                        writeContext(j, i, whichGram, iter, posforj,
                                                                     extra="updateToNotRight", cpiintI=cpI[intI])
                                                cpI[intI] = tuple((j[0], posforj))
                                                countDifGTest[whichGram][iter] = countDifGTest[whichGram][
                                                                                     iter] + 1  # 1 is the normal 3 gram
                                            if posforj == j[1]:
                                                countInitialRight += 1
                                                countDifGRight[whichGram][iter] = countDifGRight[whichGram][
                                                                                      iter] + 1
                                            elif posforj != "":
                                                writeContext(j, i, whichGram, iter, posforj)
                                            if posforj == "":
                                                cannotSolve = True

                    if cannotSolve:  # use the other rules
                        # for gram_gram, gram_p, p_g, p_p, g_, _g, p_, _p
                        listJ = build3Gram(intI, cpI, j=cpI[intI])  # build the 3 Gram with the cpI
                        ngramT = ngramRawLineGGP(listJ, [], 2)  # gram_gram
                        whichGram = 9
                        if not ruleAndResult(listJ, ngramT, dictOfngram, j, countInitialRight, countDifGTest,
                                             countDifGRight, totalUpdate, totalUpdateToRight, totalUpdateToWrong,
                                             whichGram, pos=1, countPos=3, intI=intI, iteration=iter, i=i):
                            ngramTR = ngramRawLineGGP(listJ, [3], 2)  # gram_pos
                            whichGramR = 10
                            ngramTL = ngramRawLineGGP(listJ, [1], 2)  # pos_gram
                            whichGramL = 11
                            posL = 1
                            posR = 1
                            if not ruleMoreAndResultMore(listJ, ngramTL, ngramTR, dictOfngram, j, countInitialRight,
                                                         countDifGTest, countDifGRight, totalUpdate, totalUpdateToRight,
                                                         totalUpdateToWrong, whichGramL, whichGramR, posL, posR,
                                                         countPos=3, intI=intI, iteration=iter, i=i):
                                ngramT = ngramRawLineGGP(listJ, [1, 3], 2)  # pos_pos
                                whichGram = 12
                                if not ruleAndResult(listJ, ngramT, dictOfngram, j, countInitialRight,
                                                     countDifGTest,
                                                     countDifGRight, totalUpdate, totalUpdateToRight,
                                                     totalUpdateToWrong, whichGram, pos=1, countPos=3, intI=intI,
                                                     iteration=iter, i=i):
                                    [listTwor, listTwol] = build2Gram(intI, i, j=i[intI])  # get two gram
                                    ngramT = ngramRawLineGGP(listTwor, [],
                                                             2)  # gram_  whichUsePOS, linePosition, start from 1
                                    whichGram = 13
                                    if not ruleAndResult(listJ, ngramT, dictOfngram, j, countInitialRight,
                                                         countDifGTest,
                                                         countDifGRight, totalUpdate, totalUpdateToRight,
                                                         totalUpdateToWrong, whichGram, pos=1, countPos=2, intI=intI,
                                                         iteration=iter,
                                                         i=i):  # countPos and pos is different from the others start from 0, pos is the position of the target word, start from 0
                                        ngramT = ngramRawLineGGP(listTwol, [],
                                                                 1)  # _gram whichUsePOS, linePosition, start from 1
                                        whichGram = 14
                                        if not ruleAndResult(listJ, ngramT, dictOfngram, j, countInitialRight,
                                                             countDifGTest,
                                                             countDifGRight, totalUpdate, totalUpdateToRight,
                                                             totalUpdateToWrong, whichGram, pos=0, countPos=2,
                                                             intI=intI,
                                                             iteration=iter,
                                                             i=i):  # pos: position of target word; countPos: the count attribute 's  position
                                            ngramT = ngramRawLineGGP(listTwor, [1],
                                                                     2)  # pos_, whichUsePOS, linePosition, start from 1
                                            whichGram = 15
                                            if not ruleAndResult(listJ, ngramT, dictOfngram, j, countInitialRight,
                                                                 countDifGTest,
                                                                 countDifGRight, totalUpdate, totalUpdateToRight,
                                                                 totalUpdateToWrong, whichGram, pos=1, countPos=2,
                                                                 intI=intI,
                                                                 iteration=iter,
                                                                 i=i):  # pos: position of target word; countPos: the count attribute 's  position start from 0
                                                ngramT = ngramRawLineGGP(listTwol, [2],
                                                                         1)  # a_pos, whichUsePOS, linePosition, start from 1
                                                whichGram = 16
                                                if not ruleAndResult(listJ, ngramT, dictOfngram, j,
                                                                     countInitialRight,
                                                                     countDifGTest,
                                                                     countDifGRight, totalUpdate, totalUpdateToRight,
                                                                     totalUpdateToWrong, whichGram, pos=0, countPos=2,
                                                                     intI=intI,
                                                                     iteration=iter,
                                                                     i=i):  # pos: position of target word; countPos: the count attribute 's  position start from 0
                                                    # use NNP
                                                    posforj = "NNP"
                                                    whichGram = 18
                                                    if cpI[intI][1] != posforj:
                                                        totalUpdate[whichGram][iter] = totalUpdate[whichGram][
                                                                                           iter] + 1
                                                        if posforj == j[1]:
                                                            totalUpdateToRight[whichGram][iter] += 1
                                                            writeContext(j, i, whichGram, iter, posforj,
                                                                         extra="updateToRight", cpiintI=cpI[intI])
                                                        elif cpI[intI][1] == j[1]:
                                                            totalUpdateToWrong[whichGram][iter] += 1
                                                            writeContext(j, i, whichGram, iter, posforj,
                                                                         extra="updateToNotRight", cpiintI=cpI[intI])
                                                    cpI[intI] = tuple((j[0], posforj))
                                                    countDifGTest[whichGram][0] = countDifGTest[whichGram][
                                                                                      0] + 1
                                                    if posforj == j[1]:
                                                        countInitialRight += 1
                                                        countDifGRight[whichGram][0] += 1
                                                    elif posforj != "":
                                                        writeContext(j, i, whichGram, iter, posforj)

"""
print(countDifGTest)
print(countDifGRight)
print(sum(countDifGTest))
print(sum(countDifGRight))
import pandas as pd

print(pd.DataFrame(countDifGRight,
                   index=["Right", "3Gram", "GramGramPOS", "PGG", "PGP", "GGLeftRight", "PG", "GP","Suffix5", "Suffix4", "Suffix3", "Suffix2",
                          "Suffix1", "NNP", "CD","Gram", "Suf", "G_G","G"]))
print(pd.DataFrame(countDifGTest,
                   index=["Test", "3Gram", "GramGramPOS", "PGG", "PGP", "GGLeftRight", "PG", "GP","Suffix5", "Suffix4", "Suffix3", "Suffix2",
                          "Suffix1", "NNP", "CD","Gram", "Suf", "G_G","G"]))
print(" one word ")
print(oneWordSum)
print(oneWordRight)
print(wordNum)
"""
df1 = pd.DataFrame(countDifGRight,
                   index=["Right", "3Gram", "GramGramPOS", "PGG", "PGP", "GGLeftRight", "PG", "GP","Suffix5", "Suffix4", "Suffix3", "Suffix2",
                          "Suffix1", "NNP", "CD","Gram", "Suf", "G_G","G"])
df2 = pd.DataFrame(countDifGTest,
                   index=["Test","3Gram", "GramGramPOS", "PGG", "PGP", "GGLeftRight", "PG", "GP","Suffix5", "Suffix4", "Suffix3", "Suffix2",
                          "Suffix1", "NNP", "CD","Gram", "Suf", "G_G","G"])

for i in range(df1.shape[0]):
    print(df1.iloc[[i]].index.tolist()[0], end=' ')
    for j in range(df1.shape[1]):
        print(df1.iat[i, j], end=' ')
    print(" ")
    print(df1.iloc[[i]].index.tolist()[0], end=' ')
    for j in range(df1.shape[1]):
        print(df2.iat[i, j], end=' ')
    print(" ")
    print(df1.iloc[[i]].index.tolist()[0], end=' ')
    for j in range(df1.shape[1]):
        print(df1.iat[i, j] / df2.iat[i, j], end=' ')
    print(" ")

print(pd.DataFrame(totalUpdate,
                   index=["Test", "3Gram", "GramGramPOS", "PGG", "PGP", "GGLeftRight", "PG", "GP", "Suffix3", "Suffix2",
                          "Suffix1", "NNP", "CD", "G_", "_G", "P_", "_P", "Suffix", "NNP"]))
print(pd.DataFrame(totalUpdateToRight,
                   index=["Test", "3Gram", "GramGramPOS", "PGG", "PGP", "GGLeftRight", "PG", "GP", "Suffix3", "Suffix2",
                          "Suffix1", "NNP", "CD", "G_", "_G", "P_", "_P", "Suffix", "NNP"]))
print(pd.DataFrame(totalUpdateToWrong,
                   index=["Test", "3Gram", "GramGramPOS", "PGG", "PGP", "GGLeftRight", "PG", "GP", "Suffix3", "Suffix2",
                          "Suffix1", "NNP", "CD", "G_", "_G", "P_", "_P", "Suffix", "NNP"]))
print(sum(totalUpdate))
print(sum(totalUpdateToRight))
print(sum(totalUpdateToWrong))

"""
