from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
def getStudents(url):
    try:
        html = urlopen(url)
    except (HTTPError, URLError) as e:
        print('HTTPError / URLError')
        return None
    try:
        bsObj = BeautifulSoup(html.read(), "html.parser")
        students = bsObj.find("div", {"class":"c_news"}).findAll("a")
        menus = bsObj.find(id = 'menu').findAll('a')
        #students = bsObj.body
    except AttributeError as e:
        print('AttributeError')
        return None
    for name in students:
        print(name.get_text())
    print('\n\n')
    for menu in menus:
        print(menu.get_text())
#    return students

#students = getStudents("http://em.scnu.edu.cn/jingguanren/xueshengpian/2.html")
#if students == None:
#    print("404")
#else:
#    #xprint(students)
#    for name in students:
#        print(name.get_text())


#html = urlopen("http://pythonscraping.com/pages/page1.html")
#print(html.read())
