from newspaper import Article
 
# url = "https://edition.cnn.com/2021/05/10/politics/colonial-ransomware-attack-explainer/index.html" 
url = "https://t.co/0qr5fgfzgE"
# download and parse article
article = Article(url)
article.download()
article.parse()
 
# print article text
print(article.text)
