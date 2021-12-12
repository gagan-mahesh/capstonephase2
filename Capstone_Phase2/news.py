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
# cnn_url='https://edition.cnn.com/style/article/van-gogh-meules-de-ble-painting/index.html?utm_medium=social&utm_source=twCNN&utm_term=link&utm_content=2021-10-19T05%3A01%3A05'
# cnn_url="https://edition.cnn.com/2021/06/08/europe/bubble-barrier-sea-c2e-spc-intl/index.html"
# cnn_url="https://t.co/Au1AQCGnQQ?amp=1"
# cnn_url="https://edition.cnn.com/2021/10/22/europe/italy-vaccine-pass-fascism-intl-cmd/index.html?utm_term=image&utm_medium=social&utm_source=twCNN&utm_content=2021-10-22T09%3A20%3A04"
cnn_url="https://indianexpress.com/article/opinion/editorials/covid-19-vaccine-optimism-100-crore-vaccines-7585702/"
html = requests.get(cnn_url)
bsobj = soup(html.content,'lxml')
article=""
for news in bsobj.findAll('div',{'id':'pcl-full-content'}):
    data=news.text.strip()
    data.encode("ascii", "ignore")
    # data.replace(""," ")
    # print(data)
    article+=data
print(article)