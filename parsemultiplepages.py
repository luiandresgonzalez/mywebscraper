# MyTXT.xyz parser 2.0 beta
# Parsea múltiples páginas del sitio y extrae títulos y links de descarga, entre
# otras cosas.


import csv
import requests
import re

from bs4 import BeautifulSoup

################################################
# INIT VALUES. Change these parameters
################################################
# - Filename with csv extension
# filename = "science-1-50.csv"

# the starting pages
lower_bound = 301

# the REAL amount of pages [TODO] detect this automatically
amount_pages = 400

# A string for a search pattern. Set to None if using category mode
search_for = None

# A string for search pattern
category = "science"

# Prueba
if(search_for is None):
    filename = category + "-" + str(lower_bound) + "-" + str(amount_pages) + ".csv"
    print("Category mode:", category)
else:
    filename = search_for + "-" + str(lower_bound) + "-" + str(amount_pages) + ".csv"
    print("Search mode:", search_for)
################################################

fh = open(filename, "w", encoding = 'utf-8')

fh.write("Title")
fh.write("\t")
fh.write("Author")
fh.write("\t")
fh.write("Genre")
fh.write("\t")
fh.write("Language")
fh.write("\t")
fh.write("Year")
fh.write("\t")
fh.write("Format")
fh.write("\t")
fh.write("Size")
fh.write("\t")
fh.write("Link")
fh.write("\n")

def createListOfLinks(pages_amount,search_pattern,category):
    print("Getting links to books...")
    linkList = []
    my_n_pages = pages_amount + 1
     # Starts at page 1, number of pages plus one
    for i in range(lower_bound, pages_amount + 1):
        print(round(i-lower_bound/(pages_amount-lower_bound)*100,2),"% complete",end="\r")
        # Skip page 0
        if(i == 0):
            continue
        # Los corchetes van a ser reemplazados por el número de página del
        # iterador.
        if(search_pattern is None):
            # of type https://mytxt.xyz/animals/page/1/
            # print("Searching for books in the category", category)
            url = "https://mytxt.xyz/{}/page/{}/".format(category,i)
            print(url)
        else:
            # of type https://mytxt.xyz/page/1/?s=python
            # print("Searching for books with search mode", search_pattern)
            url = "https://mytxt.xyz/page/{}/?s={}".format(i,search_pattern)
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")

        divs = soup.find_all('div', class_="media-body")
        for div in divs:
            link = div.a["href"]
            linkList.append(link)
    print("Found", len(linkList), "links to book pages")
    return linkList

def getDownloadLink(lista):

    urls = lista
    urls_length = len(urls)
    print("Getting books links from", urls_length, "urls.")

    # linklista = {}
    titleList = []
    authorlist = []
    genrelist = []
    langList = []
    yearList = []
    formatList = []
    downloadList = []
    sizeList = []


    # Para cada link de libro:
    for i in range(urls_length):
        print(round((i/urls_length)*100,2),"% complete", end="\r")

        url = urls[i]
        r = requests.get(url)
        # print("Getting", url)
        soup = BeautifulSoup(r.content, "html.parser")

        title = soup.find('div', class_="media")
        titulo = title.h1.get_text()

        book_data = soup.find('div', class_="col-md-9 book-info")
        lista = book_data.ul.find_all('b')
        # print(lista)
        autor = lista[0].text
        genre = lista[1].text
        lang = lista[2].text
        year = lista[3].text
        formato = lista[4].text
        size = removeMBorKB(lista[5].text)

        div = soup.find('div', class_="download")
        link = div.a["href"]

        titleList.append(titulo)
        authorlist.append(autor)
        genrelist.append(genre)
        langList.append(lang)
        yearList.append(year)
        formatList.append(formato)
        sizeList.append(size)
        downloadList.append(link)

        # print(titulo)
        # print(autor)
        # print(lang)
        # print(year)
        # print(formato)
        # print(size)
        # print(link)

    # print(titleList, authorlist,genrelist,langList, yearList,formatList, sizeList,downloadList)
    return(titleList, authorlist,genrelist,langList, yearList,formatList, sizeList,downloadList)

def removeMBorKB(filesize):
    if 'KB' in filesize:
        result = re.sub('[^0-9]','', filesize)
        myfloat = round((float(result) / 1024),2)
    if 'MB' in filesize:
        result = re.sub('[^0-9]','', filesize)
        myfloat = result
    return str(myfloat)

## Where the code gets executed!!!!!
hola = getDownloadLink(createListOfLinks(amount_pages,search_for,category))
# print(hola)

# counter = 0
for titleList, authorlist, genrelist, langList, yearList, formatList, sizeList, linkList in zip(*hola):
    #  counter += 1
    #  print("Writing entry number", counter)
     output = "{} \t {} \t {} \t {} \t {} \t {} \t {} \t {} \n".format(titleList, authorlist, genrelist, langList, yearList, formatList, sizeList, linkList)
     fh.write(output)

print("Have a good night!")
fh.close()
