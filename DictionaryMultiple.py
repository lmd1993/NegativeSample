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
           #input("Press Enter to continue...")
           # print(i[1])
    for i in removeL:
        l.remove(i)
    return l
def cleanAppendBeginningAndEnd(l):
    removeL = []
    for i in l:
        if i[1] == '-NONE-':
            removeL.append(i)
           # input("Press Enter to continue...")
           # print(i[1])
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
def ngramRawSuffixUpperCaseHyphen(listofNgram, nsuffix):
    temp = ""
    ii = 0
    for i in listofNgram:
        ii += 1
        if ii == 1 or ii == 3:
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
    return temp
def ngramRawGGP(listofNgram, whichPOS): # gram gram pos
    temp = ""
    which = 0
    for i in listofNgram:
        which+=1
        if which in whichPOS:
            temp += i[1]
        else:
            temp += i[0]
        temp += " "
    temp = ' '.join(temp.split())
    if "|" in temp:  # since we use the | later to split
        temp = temp.replace("|", "&")
    return temp
def ngramRawGUnderlineP(listofNgram, whichPOS, whichUnderline): # gram gram pos
    temp = ""
    which = 0
    for i in listofNgram:
        which+=1
        if which in whichPOS:
            temp += i[1]
        elif which == whichUnderline:
            temp += "_"
        else:
            temp += i[0]
        temp += " "
    temp = ' '.join(temp.split())
    if "|" in temp:  # since we use the | later to split
        temp = temp.replace("|", "&")
    return temp

def ngramRawFor1 (listofNgram):
    temp = listofNgram[0]
    return temp
def for1g(listOfTGram):

    dict = {}
    for i in listOfTGram:
        pos2 = i.split("|")[0]
        count =int(i.split("|")[1])
        if pos2 in dict:
            dict[pos2] = dict[pos2] + count
        else:
            dict[pos2] = count
    return max(dict, key=dict.get)
def for2gR(listOfTGram):
    dict = {}
    for i in listOfTGram:
        pos2 = i.split("|")[1]
        count =int(i.split("|")[2])
        if pos2 in dict:
            dict[pos2] = dict[pos2] + count
        else:
            dict[pos2] = count
    return [max(dict, key=dict.get), max(dict.values())]
def for2gL(listOfTGram):
    dict = {}
    for i in listOfTGram:
        pos2 = i.split("|")[0]
        count =int(i.split("|")[2])
        if pos2 in dict:
            dict[pos2] = dict[pos2] + count
        else:
            dict[pos2] = count
    return [max(dict, key=dict.get), max(dict.values())]
def for3g(listOfTGram):

    dict = {}
    for i in listOfTGram:
        pos2 = i.split("|")[1]
        count =int(i.split("|")[3])
        if pos2 in dict:
            dict[pos2] = dict[pos2] + count
        else:
            dict[pos2] = count
    return max(dict, key=dict.get)
def listReplace (l, newStr, oldStr):
    for i, word in enumerate(l):
        if word == oldStr:
            l[i] = newStr
    return l
def update(dictOfngram, ngramT, id, ngr, whichGr): # key: ngramT; value: id
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
            #print(ngramT)
            #print(listOfTGram)
    else:
        id = id + str(1)
        dictOfngram[whichGr][ngramT] = [id]
def build3Gram (intI, i, j):
    listJ = []
    if intI == 0:  # first word
        listJ.append(('$$', 'Begin'))
        listJ.append(j)
        if intI + 1 >= len(i):
            print(i)

        else:
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
def build2Gram (intI, i, j):
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
dictOfngram = [{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}] # 1, 3 gram; 2, gram gram POS; 3, POS gram gram; 4, POS gram POS; 5, POS gram; 6, gram POS; 7, POS _ POS
# 8, gram _ gram;

# a = ["%.2d" % i for i in range(19)]
#
# # for 3/1 gram the id is raw text: word a b c; the value is a list of value {POSa| POSb| POSc|count}
# # for gram gram POS, POS gram gram, POS gram POS, POS gram, gram POS
# for aa in a:
#     lis = glob.glob("/home/lmd1993/TREEBANK_3/MRG/WSJ/" + str(aa) + "/*.MRG")
#     # lis = ["/Users/MingdaLi/Desktop/ucla_8/ex"]
#     for lisStr in lis:
#         print(lisStr)
with open("convertedStanfordTagTrainEnglish2", "r") as ins:
    for line in ins:
        checkR = []
        if line != '\n':
            line = line.replace(' \n', '')
            linArr = line.split(' ')
            #print(line)
            for j in linArr:
                #print(j)
                if '_' in j:
                    checkR.append((j.split('_')[0], j.split('_')[1]))
            i = checkR
            i = cleanAppendBeginningAndEnd(i)
            # for 1. 3 Gram
            ngr = 3
            whichGr = 1 # id of dict
            for j in list(ngrams(i, ngr, 0)):
                ngramT = ngramRaw(j)  # key
                if "|" in ngramT: # since we use the | later to split
                    ngramT = ngramT.replace("|", "&")
                posII = 0
                id = ""
                while posII < ngr:
                    id = id + j[posII][1] + "|" # id is the value of the key
                    posII = posII + 1
                update(dictOfngram, ngramT, id, ngr, whichGr)
            # for 2-1. gram gram POS: right to left
            ngr = 3
            whichGr = 2
            whPOS = [3]
            for j in list(ngrams(i, ngr, 0)):
                ngramT = ngramRawGGP(j, whPOS)  # key
                if "|" in ngramT: # since we use the | later to split
                    ngramT = ngramT.replace("|", "&")
                posII = 0
                id = ""
                while posII < ngr: # can be optimize, removed the third POS which is fixed
                    id = id + j[posII][1] + "|" # id is the value of the key
                    posII = posII + 1
                update(dictOfngram, ngramT, id, ngr, whichGr)
            # for 2-2. POS gram gram: left to right
            ngr = 3
            whichGr = 3
            whPOS = [1]
            for j in list(ngrams(i, ngr, 0)):
                ngramT = ngramRawGGP(j, whPOS)  # key
                if "|" in ngramT:  # since we use the | later to split
                    ngramT = ngramT.replace("|", "&")
                posII = 0
                id = ""
                while posII < ngr:  # can be optimize, removed the third POS which is fixed
                    id = id + j[posII][1] + "|"  # id is the value of the key
                    posII = posII + 1
                update(dictOfngram, ngramT, id, ngr, whichGr)
            # for 3. POS gram POS: left to right
            ngr = 3
            whichGr = 4
            whPOS = [1, 3] # which use the POS but not gram
            for j in list(ngrams(i, ngr, 0)):
                ngramT = ngramRawGGP(j, whPOS)  # key
                if "|" in ngramT:  # since we use the | later to split
                    ngramT = ngramT.replace("|", "&")
                posII = 0
                id = ""
                while posII < ngr:  # can be optimize, removed the third POS which is fixed
                    id = id + j[posII][1] + "|"  # id is the value of the key
                    posII = posII + 1
                update(dictOfngram, ngramT, id, ngr, whichGr)
            # for 3-1. 2 Gram Left; 3-2. 2 Gram Right
            ngr = 2
            whichGr = 5
            for j in list(ngrams(i, ngr, 0)):
                ngramT = ngramRaw(j)  # key
                if "|" in ngramT:  # since we use the | later to split
                    ngramT = ngramT.replace("|", "&")
                posII = 0
                id = ""
                while posII < ngr:  # can be optimize, removed the third POS which is fixed
                    id = id + j[posII][1] + "|"  # id is the value of the key
                    posII = posII + 1
                update(dictOfngram, ngramT, id, ngr, whichGr)
            # for 4-1. POS gram
            ngr = 2
            whichGr = 6
            whPOS = [1]
            for j in list(ngrams(i, ngr, 0)):
                ngramT = ngramRawGGP(j, whPOS)  # key
                if "|" in ngramT:  # since we use the | later to split
                    ngramT = ngramT.replace("|", "&")
                posII = 0
                id = ""
                while posII < ngr:  # can be optimize, removed the third POS which is fixed
                    id = id + j[posII][1] + "|"  # id is the value of the key
                    posII = posII + 1
                update(dictOfngram, ngramT, id, ngr, whichGr)
            # for 4-2. gram POS
            ngr = 2
            whichGr = 7
            whPOS = [2]
            for j in list(ngrams(i, ngr, 0)):
                ngramT = ngramRawGGP(j, whPOS)  # key
                if "|" in ngramT:  # since we use the | later to split
                    ngramT = ngramT.replace("|", "&")
                posII = 0
                id = ""
                while posII < ngr:  # can be optimize, removed the third POS which is fixed
                    id = id + j[posII][1] + "|"  # id is the value of the key
                    posII = posII + 1
                update(dictOfngram, ngramT, id, ngr, whichGr)
            # for many many features we put them all here
            # suffix 5
            ngr = 3
            whichGr = 8
            for j in list(ngrams(i, ngr, 0)):
                if len(j)>=5:
                    ngramT = ngramRawSuffixUpperCaseHyphen(j, 5)
                    if "|" in ngramT:  # since we use the | later to split
                        ngramT = ngramT.replace("|", "&")
                    posII = 0
                    id = ""
                    while posII < ngr:  # can be optimize, removed the third POS which is fixed
                        id = id + j[posII][1] + "|"  # id is the value of the key
                        posII = posII + 1
                    update(dictOfngram, ngramT, id, ngr, whichGr)
            # suffix 4
            ngr = 3
            whichGr = 9
            for j in list(ngrams(i, ngr, 0)):
                if len(j) >= 4:
                    ngramT = ngramRawSuffixUpperCaseHyphen(j, 4)
                    if "|" in ngramT:  # since we use the | later to split
                        ngramT = ngramT.replace("|", "&")
                    posII = 0
                    id = ""
                    while posII < ngr:  # can be optimize, removed the third POS which is fixed
                        id = id + j[posII][1] + "|"  # id is the value of the key
                        posII = posII + 1
                    update(dictOfngram, ngramT, id, ngr, whichGr)


            # suffix 3
            ngr = 3
            whichGr = 10
            for j in list(ngrams(i, ngr, 0)):
                if len(j) >= 3:
                    ngramT = ngramRawSuffixUpperCaseHyphen(j, 3)
                    if "|" in ngramT:  # since we use the | later to split
                        ngramT = ngramT.replace("|", "&")
                    posII = 0
                    id = ""
                    while posII < ngr:  # can be optimize, removed the third POS which is fixed
                        id = id + j[posII][1] + "|"  # id is the value of the key
                        posII = posII + 1
                    update(dictOfngram, ngramT, id, ngr, whichGr)
            # suffix 2
            ngr = 3
            whichGr = 11
            for j in list(ngrams(i, ngr, 0)):
                if len(j) >= 2:
                    ngramT = ngramRawSuffixUpperCaseHyphen(j, 2)
                    if "|" in ngramT:  # since we use the | later to split
                        ngramT = ngramT.replace("|", "&")
                    posII = 0
                    id = ""
                    while posII < ngr:  # can be optimize, removed the third POS which is fixed
                        id = id + j[posII][1] + "|"  # id is the value of the key
                        posII = posII + 1
                    update(dictOfngram, ngramT, id, ngr, whichGr)

            # suffix 1
            ngr = 3
            whichGr = 12
            for j in list(ngrams(i, ngr, 0)):
                ngramT = ngramRawSuffixUpperCaseHyphen(j, 1)
                if "|" in ngramT:  # since we use the | later to split
                    ngramT = ngramT.replace("|", "&")
                posII = 0
                id = ""
                while posII < ngr:  # can be optimize, removed the third POS which is fixed
                    id = id + j[posII][1] + "|"  # id is the value of the key
                    posII = posII + 1
                update(dictOfngram, ngramT, id, ngr, whichGr)




ii = 0
for i in dictOfngram:
    if ii>=1:
        f = open("regPreDifMultipleFeatureNewPOS/dictOf"+str(ii)+"Gram", "a")
        for i, v in dictOfngram[ii].items():
            f.write(str(i) + '|' + str(v))
            f.write('\n')
        f.close()
        with open("regPreDifMultipleFeatureNewPOS/mySavedDictPOS"+str(ii)+".txt", "wb") as myFile:
            pickle.dump(dictOfngram[ii], myFile)
    ii+=1

