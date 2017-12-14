from bs4 import BeautifulSoup
import urllib2
import csv
from halo import Halo

csvfile = csv.writer(open('imdb.csv', 'w'))
csvfile.writerow(["Name", "Year of release", "Rating", "Genre", "imdb Url", "votes"])
pages = int(raw_input("enter number of pages to scrap:"))
url = 'http://www.imdb.com/search/title?genres=action'
i = 1
while pages > 0:
    request = urllib2.Request(url)
    request.add_header('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0')
    myurlopener = urllib2.build_opener()
    myurl = myurlopener.open(request)
    spinner = Halo(text="Processing Page", spinner="dots")
    spinner.start()
    myurldata = myurl.read()
    soup = BeautifulSoup(myurldata, 'lxml')
    for choice in soup.find_all('div', class_='lister-item-content'):                                   # find the and iterate over the div containing required data
        name = choice.a.text.encode('utf-8')                                                            # get the name of the movie
        imdburl = choice.a.get('href').encode('utf-8')                                                  # get the imdb url of the movie
        if not imdburl.startswith('http://www.imdb.com'):                                               # check if link is valid or not
            imdburl = "http://www.imdb.com" + imdburl
        year = choice.find('span', class_='lister-item-year').text.encode('utf-8')                      # get the year of release of the movie
        try:
            rating = choice.find('div', class_='ratings-imdb-rating').get('data-value').encode('utf-8') # get the ratings of the movie
        except AttributeError:                                                                          # if ratings not available then store "NA"
            rating = "NA"
        genre = choice.find('span', class_='genre').text.encode('utf-8')                                # get the genre of the movie
        try:
            votes = choice.find('span', {"name": 'nv'}).text.encode('utf-8')                            # get the number of votes for the movie
        except AttributeError:                                                                          # if votes not available then store "NA"
            votes = "NA"
        csvfile.writerow([name, year, rating, genre, imdburl, votes])                                   # write the fetched values to the csv file
    url = soup.find('a', class_="lister-page-next").get('href')                                         # get the url of next page to be scraped
    if not url.startswith("http://www.imdb.com/search/title"):                                          # check if url is valid or not
        url = "http://www.imdb.com/search/title" + url
    spinner.stop()
    pages = pages - 1
    print "\nPage Number " + str(i) + " complete"
    i = i + 1
print "Scraping Complete"
