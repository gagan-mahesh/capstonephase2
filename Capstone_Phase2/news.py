# from newspaper import Article
 
# # url = "https://edition.cnn.com/2021/05/10/politics/colonial-ransomware-attack-explainer/index.html" 
# url = "https://t.co/0qr5fgfzgE"
# # download and parse article
# article = Article(url)
# article.download()
# article.parse()
 
# # print article text
# print(article.text)

from bs4 import BeautifulSoup as soup
import requests
cnn_url="https://edition.cnn.com/2021/06/08/europe/bubble-barrier-sea-c2e-spc-intl/index.html"
html = requests.get(cnn_url)
bsobj = soup(html.content,'lxml')
article=""
for news in bsobj.findAll('div',{'class':'zn-body__paragraph'}):
    data=news.text.strip()
    data.encode("ascii", "ignore")
    # data.replace(""," ")
    # print(data)
    article+=data
print(article)