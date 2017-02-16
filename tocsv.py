import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen('http://em.scnu.edu.cn/a/20140711/4447.html')
tableObj = BeautifulSoup(html, 'html.parser')
table = tableObj.find('table', {'width': '345'})
rows = table.findAll('tr')
csvFile = open('./em.csv', 'wt', newline='', encoding='utf-8')
writer = csv.writer(csvFile)

try:
    for row in rows:
        csvRow = []
        for cell in row.findAll(['td', 'th']):
            csvRow.append(cell.get_text())
        writer.writerow(csvRow)
finally:
    csvFile.close()
