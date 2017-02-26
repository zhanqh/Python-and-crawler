import csv
 
sourceFile = open('references.csv')
sourceCsv = csv.reader(sourceFile)

sorted_csv = open('./sorted.csv', 'wt', newline='', encoding='utf-8')
writer = csv.writer(sorted_csv)

source_list = []
for row in sourceCsv:
    source_list.append(row)

names = []
for row in source_list:
    names.append(row[0])

names.sort()

sorted_lsit = []
for name in names:
    for row in source_list:
        if row[0] == name:
            row.pop(0)
            s = row[0]
            row[0] = '[' + str(names.index(name)+1) + ']' + s[(s.index(']')+1):]
            print('[' + str(names.index(name)+1) + ']' + s[(s.index(']')+1):])
            sorted_lsit.append(row)

try:
    for x in sorted_lsit:
        writer.writerow(x)
finally:
    sorted_csv.close()
