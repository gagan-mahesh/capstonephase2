from transformers import T5Tokenizer, TFT5Model, TFT5ForConditionalGeneration
import tensorflow as tf
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
import pandas as pd
import re
import numpy as np
from newspaper import Article
from tweepySample import *

tokenizer = T5Tokenizer.from_pretrained('./Abstractive Summarisation model/summarisation_tokeniser')
model = TFT5ForConditionalGeneration.from_pretrained('./Abstractive Summarisation model/summarisation_model')


def decontracted(phrase):
    # specific
    phrase = re.sub(r"won't", "will not", phrase)
    phrase = re.sub(r"can\'t", "can not", phrase)
    # general
    phrase = re.sub(r"n\'t", " not", phrase)
    phrase = re.sub(r"\'re", " are", phrase)
    phrase = re.sub(r"\'s", " is", phrase)
    phrase = re.sub(r"\'d", " would", phrase)
    phrase = re.sub(r"\'ll", " will", phrase)
    phrase = re.sub(r"\'t", " not", phrase)
    phrase = re.sub(r"\'ve", " have", phrase)
    phrase = re.sub(r"\'m", " am", phrase)
    return phrase


def cleanText(article):
    tt=re.sub(r'\n',' ',article)
    tt=re.sub(r'>',' ', tt)
    tt=re.sub(r'<',' ', tt)
    tt=re.sub(r'(CNN)',' ', tt)
    tt=re.sub(r'LRB',' ', tt)
    tt=re.sub(r'RRB',' ', tt)
    tt = re.sub(r'[" "]+', " ", tt)
    tt=re.sub(r'-- ',' ', tt)
    tt=re.sub(r"([?!¿])", r" \1 ", tt)
    tt=re.sub(r'-',' ', tt)
    tt=tt.replace('/',' ')
    tt=re.sub(r'\s+', ' ', tt)
    tt=decontracted(tt)
    tt = re.sub('[^A-Za-z0-9.,]+', ' ', tt)
    tt = tt.lower()
    return tt


# In[5]:


def summarize(article):
    ids =tokenizer.encode_plus((model.config.prefix + article), return_tensors="tf", max_length=512)
    sum = model.generate(input_ids=ids['input_ids'], attention_mask=ids['attention_mask'],min_length=100)
    pred = [tokenizer.decode(g, skip_special_tokens=True, clean_up_tokenization_spaces=False) for g in sum]
    return ' '.join(pred)


# In[6]:


def returnSummary(article):
    result =decontracted(article)
    return summarize(cleanText(result))



def get_article(url):
    #url = "https://edition.cnn.com/2021/05/10/politics/colonial-ransomware-attack-explainer/index.html" 
    # download and parse article
    article = Article(url)
    article.download()
    article.parse()
    
    #removing new line and making the input into proper format
    res = ""
    content = article.text
    content = content.split("\n")
    for line in content:
        res += line.strip()+"."
    return res

def get_summary():
    global res
    list_of_articles = get_tweets("CNN")
    list_of_summary = []
    for i in list_of_articles:
        article = get_article(i)
        summary = returnSummary(article)
        list_of_summary.append(summary)
    #print(summary)
    return list_of_summary
