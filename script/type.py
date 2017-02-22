# 参考 source.csv 文件中 code 与 Nnindcd 的对应关系，匹配 untype.csv 中 code 的对应值，输出到 typed.csv 文件
# 坑：csv 文件读到 Python 中后是 Generator 生成器的数据结构，只能遍历一次，而无法重复遍历，因而必须将其处理成能够循环遍历的 list 类型。

import csv

source_file = open('source.csv')
source_csv = csv.reader(source_file)

untype_file = open('untype.csv')
untype_csv = csv.reader(untype_file)

typed_csv = open('./typed.csv', 'wt', newline='', encoding='utf-8')
writer = csv.writer(typed_csv)

source_list = []
for row in source_csv:
    source_list.append(row)
untype_list = []
for row in untype_csv:
    untype_list.append(row)

try:
    for row2 in untype_list:
        csvRow = []
        for row1 in source_list:
            if row2[0] == row1[0]:
                csvRow.append(row2[0])
                csvRow.append(row1[1])
        writer.writerow(csvRow)
finally:
    typed_csv.close()
