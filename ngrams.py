import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import string
import operator

def cleanInput(input):
    input = re.sub('\n+', " ", input).lower()    # 一个及以上换行符替换成空格
    input = re.sub('\[[0-9]*\]', "", input)    # 删除引用标记
    input = re.sub(' +', " ", input)    # 将连续多个空格替换成一个空格
    input = bytes(input, 'UTF-8')
    input = input.decode('ascii', 'ignore')
    cleanInput = []
    input = input.split(' ')
    for item in input:
        item = item.strip(string.punctuation)    # 移除字符串首位的标点符号
        if len(item) > 1 or (item.lower() == 'a' or item.lower() == 'i'):
            cleanInput.append(item)
    return cleanInput

def isCommon(ngram):
    commonWords = ["the", "be", "and", "of", "a", "in", "to", "have", "it", "i", "that", "for", "you", "he", "with", "on", "do", "say", "this", "they", "is", "an", "at", "but","we", "his", "from", "that", "not", "by", "she", "or", "as", "what", "go", "their","can", "who", "get", "if", "would", "her", "all", "my", "make", "about", "know", "will", "as", "up", "one", "time", "has", "been", "there", "year", "so", "think", "when", "which", "them", "some", "me", "people", "take", "out", "into", "just", "see", "him", "your", "come", "could", "now", "than", "like", "other", "how", "then", "its", "our", "two", "more", "these", "want", "way", "look", "first", "also", "new", "because", "day", "more", "use", "no", "man", "find", "here", "thing", "give", "many", "well"]
    for word in ngram.split(' '):
        if word in commonWords:
            return True
    return False

def ngrams(input, n):
    input = cleanInput(input)
    output = {}
    a = 0
    b = 0
    c = 0
    for i in range(len(input) - n + 1):
        ngramTemp = ' '.join(input[i : i + n])
        if isCommon(ngramTemp):
            #print('is common')
            a += 1
            pass
        else:
            b += 1
            if ngramTemp not in output:
                output[ngramTemp] = 0
            output[ngramTemp] += 1
    print(a)
    print(b)
    #     c += 1
    #     if ngramTemp not in output:
    #         output[ngramTemp] = 0
    #     output[ngramTemp] += 1
    # print(c)
    return output

content = str(urlopen('http://www.pythonscraping.com/files/inaugurationSpeech.txt').read(), 'utf-8')
ngrams = ngrams(content, 2)
sortedNGrams = sorted(ngrams.items(), key = operator.itemgetter(1), reverse = True)
#print(sortedNGrams)
csvFile = open('./2grams.csv', 'wt', newline='', encoding='utf-8')
writer = csv.writer(csvFile)
writer.writerow(['分词', '频率'])
try:
    for item in sortedNGrams:
        csvRow = []
        for cell in item:
            csvRow.append(cell)
        writer.writerow(csvRow)
finally:
    csvFile.close()
