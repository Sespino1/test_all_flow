import requests, os, bs4, webbrowser, re, urllib, openpyxl
#read from csv file
all_flow_book = openpyxl.load_workbook('all_flow.xlsx')
type(all_flow_book)
sheet=all_flow_book.get_active_sheet()
for i in range(2,1886): #1885 files
    print(i, sheet.cell(row=i,column = 1).value)  #gets value in cell to set as sku
    sku= sheet.cell(row=i,column = 1).value

    url = 'http://www.all-flo.com/search.html?q='+sku

    #webbrowser.open(url)
    res = requests.get(url) #requests the url previously saved
    res.raise_for_status()  #checks that no errors have occured
    soup = bs4.BeautifulSoup(res.text)
    type(soup)

    skuData = soup.select('.onesearchresult a')
    print(str(skuData[0]))  #link of element

    searchUrl = str(skuData[0])
    print(searchUrl)

    def extractLinks(searchUrl):
        soup = bs4.BeautifulSoup(searchUrl)
        anchors = soup.findAll('a')
        links = []
        for a in anchors:
            links.append(a['href'])
        return links[0]

    searchUrl = extractLinks(searchUrl)  #link has been extracted
    print(searchUrl)
    newUrl = 'http://www.all-flo.com'+searchUrl
    #webbrowser.open(newUrl)

    print ('Downloading description for %s...' % newUrl)
    res = requests.get(newUrl) #requests the url previously saved
    res.raise_for_status()  #checks that no errors have occured
    weightSoup = bs4.BeautifulSoup(res.text)

    weights = weightSoup.select('#specsdata')
    print(weights[0].getText())
    descriptionFile = open('Descriptions', "a")
    descriptionFile.write(sku+'\n')
    descriptionFile.write(weights[0].getText())
    descriptionFile.write("\n")

    print('Done\n\n')
descriptionFile.close()

