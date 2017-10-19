#! /usr/bin/env python3
import requests, bs4, sys, re
#get download link
def getDownloadLink(movieList):
	count = 1
	for link in movieList:
		detailLink = baseUrl+link['href']
		moviePage = requests.get(detailLink)
		# moviePage.encoding='gb2312'
		moviePage.encoding='GBK'
		moviePage.raise_for_status()

		movieSoup = bs4.BeautifulSoup(moviePage.text, "lxml")
		downloadLinkEle = movieSoup.select('td[bgcolor="#fdfddf"]')
		movieName = link.text
		if len(downloadLinkEle) != 0:
			extractedURL = downloadLinkEle[0].text
			print("{}.name: {}".format(count, movieName))
			print(extractedURL)
			count += 1

def findNextLink(soup):
  	nextPageEles = soup.select('a[href^="list_23_]"')
  	getTotalPages(soup)
  	return nextPageEles[-2]['href']

def getTotalPages(soup):
	entryEle = soup.select('td[bgcolor="#F4FAE2"]')
	entry = entryEle[0].text
	splitRegex = re.compile(r'\s+')
	splitText = splitRegex.split(entry)
	return int(splitText[-2])
	

url = 'http://www.dytt8.net/html/gndy/dyzz/'
baseUrl = 'http://www.dytt8.net/'
nextPageLink = url
# define the num of pages to view
pagesToView = 2 
total = 0

numOfArgs = len(sys.argv)
if numOfArgs == 2:
	pagesToView = int(sys.argv[1])

print("Num of pages to view: {}".format(pagesToView))

for i in range(pagesToView):
	res = requests.get(nextPageLink)
	# read the website code
	# res.encoding='gb2312'
	res.encoding='GBK'
	res.raise_for_status() 
	soup = bs4.BeautifulSoup(res.text, "lxml")
	if i == 0:
		total = getTotalPages(soup)
		print('Total: {}'.format(total))
	tables = soup.select('a.ulink')
	print("Page: {}/{}".format(i+1, pagesToView))
	
	getDownloadLink(tables)
	nextPart = findNextLink(soup)
	nextPageLink = "{}{}".format(url, nextPart)









