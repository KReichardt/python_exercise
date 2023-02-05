import urllib.request as urllib2
from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from string import punctuation
from nltk.probability import FreqDist

homePageUrl = "https://www.glanos.de/blog/"
articles = []


# Erstellen einer Liste von URLs zu allen Blogeinträgen, die auf einer Seite verlinkt sind:
def getListOfUrl(url):
    homePage = urllib2.urlopen(url).read().decode('utf8', 'ignore')
    homeSoup = BeautifulSoup(homePage, 'lxml')
    links = list()

    for link in homeSoup.find_all("a"):
        if link.get("title"):
            links.append(link.get("href"))
    if not len(links):
        print("No links found.")
        exit()
    urlList = list(set(links))
    return urlList


# Extraktion der Blogartikel auf der jeweiligen Seite als String:
def getTextFromUrl(url):
    articleList = []
    page = urllib2.urlopen(url).read().decode('utf8', 'ignore')
    soup = BeautifulSoup(page, 'lxml')
    results = soup.find_all('p')
    for result in results:
        articleList.append(result.text)
    article = "".join(articleList)
    return article


urlList = getListOfUrl(homePageUrl)
for link in urlList:
    content = getTextFromUrl(link)
    articles.append(content)

article = "".join(articles)

# Weiterverarbeitung der extrahierten Blogseiten
# Ausgabe der 10 Häufigsten Wörter in allen Blogartikeln

words = word_tokenize(article)
ownStopWords = ["„", "“", "–", "”"] # Eigene Liste mit Satzzeichen, die in importierter Liste fehlten
stopwords = set(stopwords.words('german') + stopwords.words('english') + list(punctuation) + ownStopWords) # Liste mit Stopwords auf Deutsch und Englisch und Satzzeichen
words = [word for word in words if word.lower() not in [stopword.lower() for stopword in stopwords]]    # Stopwords und Satzzeichen sollen in Häufigkeitsliste ignoriert werden
freq = FreqDist(words)
print(freq.most_common(10))

