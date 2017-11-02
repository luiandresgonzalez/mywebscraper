import csv
import requests
import re

from bs4 import BeautifulSoup

################################################
# INIT VALUES. Change these parameters
################################################

# What is the first page to be scraped?
lower_bound = 301

# What is the last page to be scraped? [TODO] detect this automatically
upper_bound = 310

# A string for a search pattern. Set to None if using category mode
search_for = None

# A string for search pattern
category = "science"
################################################

# Setting the filename
if(search_for is None):
    filename = category + "-" + str(lower_bound) + "-" + str(upper_bound) + ".csv"
    print("Category mode:", category)
else:
    filename = search_for + "-" + str(lower_bound) + "-" + str(upper_bound) + ".csv"
    print("Search mode:", search_for)

# Opening the filename connection and writing the headers
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

def main():
    # Get the list of books
    listOfBooks = createListOfLinks(upper_bound,lower_bound,search_for,category)

    # Get the download links and other stuff from the list of book links
    listofLinks = getDownloadLink(listOfBooks)

    # counter = 0
    for titleList, authorlist, genrelist, langList, yearList, formatList, sizeList, linkList in zip(*listofLinks):
        #  counter += 1
        #  print("Writing entry number", counter)
        output = "{} \t {} \t {} \t {} \t {} \t {} \t {} \t {} \n".format(titleList, authorlist, genrelist, langList, yearList, formatList, sizeList, linkList)
        fh.write(output)

        print("Have a good night!")


# createListOfLinks:
# Takes the parameters and returns a list of the links that contains both
# the book data and the download link.
def createListOfLinks(upper_bound,lower_bound,search_pattern,category):
    print("Getting links to books...")
    linkList = []
    my_n_pages = upper_bound + 1
     # Starts at page 1, number of pages plus one
    for i in range(lower_bound, upper_bound + 1):
        print(round((i-lower_bound)/(upper_bound-lower_bound)*100,2),"% complete",end="\r")
        # Skip page 0
        if(i == 0):
            continue

        # The curly brackets will be replaced by category and page numbers
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

def getDownloadLink(booksUrls):

    urls = booksUrls
    urls_length = len(urls)
    print("Getting books links from", urls_length, "urls.")

    titleList = []
    authorlist = []
    genrelist = []
    langList = []
    yearList = []
    formatList = []
    downloadList = []
    sizeList = []

    # For each book link:
    for i in range(urls_length):
        print(round((i/urls_length)*100,2),"% complete", end="\r")

        url = urls[i]
        r = requests.get(url)
        # print("Getting", url)
        soup = BeautifulSoup(r.content, "html.parser")

        title = soup.find('div', class_="media")
        titulo = title.h1.get_text()

        book_data = soup.find('div', class_="col-md-9 book-info")
        book_data_list = book_data.ul.find_all('b')
        # print(book_data_list)
        autor = book_data_list[0].text
        genre = book_data_list[1].text
        lang = book_data_list[2].text
        year = book_data_list[3].text
        formato = book_data_list[4].text
        size = removeMBorKB(book_data_list[5].text)

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

# About this https://www.youtube.com/watch?v=sugvnHA7ElY. Thanks /u/Rorixrebel and /u/ykcmaster
if __name__ == '__main__':
    main()

fh.close()
