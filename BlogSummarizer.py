import urllib.request as urllib2
from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from string import punctuation
from nltk.probability import FreqDist
from heapq import nlargest
from collections import defaultdict, namedtuple

homePageUrl = "https://www.glanos.de/blog/"
articles = []
UrlTupel = namedtuple('UrlTupel', 'title link')
ArticleTupel = namedtuple('ArticleTupel', 'title text')

# Erstellen einer Liste von URLs zu allen Blogeinträgen, die auf einer Seite verlinkt sind, inkl. Titel:
def getListOfUrl(url):
    homePage = urllib2.urlopen(url).read().decode('utf8', 'ignore')
    homeSoup = BeautifulSoup(homePage, 'lxml')
    res = list()
    for link in homeSoup.find_all("a"):
        title = link.get("title")
        if title:
            resLink = UrlTupel(title, link.get("href"))
            res.append(resLink)

    urlList = list(set(res))
    return urlList


# Extraktion der Blogartikel auf der jeweiligen Seite als Liste von Tupel (Titel, Text):
def getTextFromUrl(urlList):
    articleList = list()
    for elem in urlList:
        fullArticle = []
        page = urllib2.urlopen(elem.link).read().decode('utf8', 'ignore')
        soup = BeautifulSoup(page, 'lxml')
        paragraphs = soup.find_all('p')
        for para in paragraphs:
            fullArticle.append(para.text)
        article = "".join(fullArticle)
        articleWithTitle = ArticleTupel(elem.title, article)
        articleList.append(articleWithTitle)
    return articleList


urlList = getListOfUrl(homePageUrl)
articleList = getTextFromUrl(urlList)

# Weiterverarbeitung der extrahierten Blogseiten

ownStopWords = ["„", "“", "–", "”"]  # Eigene Liste mit Satzzeichen, die in importierter Liste fehlten
stopwords = set(stopwords.words('german') + stopwords.words('english') + list(punctuation) + ownStopWords)  # Liste mit Stopwords auf Deutsch und Englisch und Satzzeichen

# Zählen der Häufigkeit der Wörter in jedem Artikel
for article in articleList:
    sentences = sent_tokenize(article.text)
    words = word_tokenize(article.text)
    words = [word for word in words if word.lower() not in [stopword.lower() for stopword in stopwords]]  # Stopwords und Satzzeichen sollen in Häufigkeitsliste ignoriert werden
    freq = FreqDist(words)

    # Ranking der Sätze durch Häufigkeit der darin enthaltenen Wörter
    ranking = defaultdict(int)
    for i, sent in enumerate(sentences):
        for w in word_tokenize(sent.lower()):
            if w in freq:
                ranking[i] += freq[w]

    # Erstellen einer Zusammenfassung der Artikel aus den drei wichtigsten Sätzen
    sentencesNumber = nlargest(3, ranking, key=ranking.get)
    sentencesSorted = [sentences[i] for i in sorted(sentencesNumber)]
    summary = "".join(sentencesSorted)
    print(article.title + ":")
    print(summary)

