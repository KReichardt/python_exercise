import urllib.request as urllib2
from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from string import punctuation
from nltk.probability import FreqDist
from heapq import nlargest
from collections import defaultdict

homePageUrl = "https://www.glanos.de/blog/"
articles = []


# Erstellen einer Liste von URLs zu allen Blogeinträgen, die auf einer Seite verlinkt sind, inkl. Titel:
def getListOfUrl(url):
    homePage = urllib2.urlopen(url).read().decode('utf8', 'ignore')
    homeSoup = BeautifulSoup(homePage, 'lxml')
    res = list()
    for link in homeSoup.find_all("a"):
        title = link.get("title")
        if title:
            resLink = (title, link.get("href"))
            res.append(resLink)

    urlList = list(set(res))
    return urlList


# Extraktion der Blogartikel auf der jeweiligen Seite als Liste von Tupel (Titel, Text):
def getTextFromUrl(urlList):
    articleList = list()
    for elem in urlList:
        fullArticle = []
        page = urllib2.urlopen(elem[1]).read().decode('utf8', 'ignore')
        soup = BeautifulSoup(page, 'lxml')
        results = soup.find_all('p')
        for result in results:
            fullArticle.append(result.text)
        article = "".join(fullArticle)
        articleWithTitle = (elem[0], article)
        articleList.append(articleWithTitle)
    return articleList


urlList = getListOfUrl(homePageUrl)
articleList = getTextFromUrl(urlList)

# Weiterverarbeitung der extrahierten Blogseiten

ownStopWords = ["„", "“", "–",
                "”"]  # eigene Stopwordliste mit Sonderzeichen, die nicht in der Liste der Bibliothek vorkamen
stopwords = set(stopwords.words('german') + stopwords.words('english') + list(punctuation) + ownStopWords)

# Zählen der Häufigkeit der Wörter in jedem Artikel
for article in articleList:
    title = article[0]
    text = article[1]
    sentences = sent_tokenize(text)
    words = word_tokenize(text)
    words = [word for word in words if word.lower() not in [stopword.lower() for stopword in stopwords]]
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
    print(title + ":")
    print(summary)

