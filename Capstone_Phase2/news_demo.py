#!/usr/bin/env python
# coding: utf-8

# In[1]:


from transformers import T5Tokenizer, TFT5Model, TFT5ForConditionalGeneration
import tensorflow as tf
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
import pandas as pd
import re
import numpy as np
from newspaper import Article



# In[2]:


tokenizer = T5Tokenizer.from_pretrained('./AbstractiveSummarisationmodel/summarisation_tokeniser')
model = TFT5ForConditionalGeneration.from_pretrained('./AbstractiveSummarisationmodel/summarisation_model')


# In[3]:


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


# In[4]:


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


# In[7]:


samp="usain bolt rounded off the world championships sunday by claiming his third gold in moscow as he anchored jamaica to victory in the men is 4x100m relay. the fastest man in the world charged clear of united states rival justin gatlin as the jamaican quartet of nesta carter, kemar bailey cole, nickel ashmeade and bolt won in 37.36 seconds. the u.s finished second in 37.56 seconds with canada taking the bronze after britain were disqualified for a faulty handover. the 26 year old bolt has now collected eight gold medals at world championships, equaling the record held by american trio carl lewis, michael johnson and allyson felix, not to mention the small matter of six olympic titles. the relay triumph followed individual successes in the 100 and 200 meters in the russian capital. i am proud of myself and i will continue to work to dominate for as long as possible, bolt said, having previously expressed his intention to carry on until the 2016 rio olympics. victory was never seriously in doubt once he got the baton safely in hand from ashmeade, while gatlin and the united states third leg runner rakieem salaam had problems. gatlin strayed out of his lane as he struggled to get full control of their baton and was never able to get on terms with bolt. earlier, jamaica is women underlined their dominance in the sprint events by winning the 4x100m relay gold, anchored by shelly ann fraser pryce, who like bolt was completing a triple. their quartet recorded a championship record of 41.29 seconds, well clear of france, who crossed the line in second place in 42.73 seconds. defending champions, the united states, were initially back in the bronze medal position after losing time on the second handover between alexandria anderson and english gardner, but promoted to silver when france were subsequently disqualified for an illegal handover. the british quartet, who were initially fourth, were promoted to the bronze which eluded their men is team. fraser pryce, like bolt aged 26, became the first woman to achieve three golds in the 100 200 and the relay. in other final action on the last day of the championships, france is teddy tamgho became the third man to leap over 18m in the triple jump, exceeding the mark by four centimeters to take gold. germany is christina obergfoll finally took gold at global level in the women is javelin after five previous silvers, while kenya is asbel kiprop easily won a tactical men is 1500m final. kiprop is compatriot eunice jepkoech sum was a surprise winner of the women is 800m. bolt is final dash for golden glory brought the eight day championship to a rousing finale, but while the hosts topped the medal table from the united states there was criticism of the poor attendances in the luzhniki stadium. there was further concern when their pole vault gold medalist yelena isinbayeva made controversial remarks in support of russia is new laws, which make the propagandizing of non traditional sexual relations among minors a criminal offense. she later attempted to clarify her comments, but there were renewed calls by gay rights groups for a boycott of the 2014 winter games in sochi, the next major sports event in russia"


# In[8]:


# print(returnSummary(samp)


# In[9]:


cnn="""Tesla's "full self-driving" feature has attempted to drive under a railroad crossing arm while a speeding train passes. It's nearly driven head on into a concrete wall of a parking garage, attempted ill-advised left turns, clipped at least one curb, and at least one driver was able to set a maximum speed of 90 mph on a street where the posted speed limit was 35 mph, according to videos posted on social media.
These drivers knew they weren't using a foolproof system, and that there would be glitches as they had agreed to test early versions of the regularly updating "full self-driving" software for Tesla. The company warned them of limitations, and their need to be attentive.
Experts worry that the name of the feature implies a greater functionality than what Tesla is actually offering. But the risks of "full self-driving" don't appear to be holding Tesla back from a broad beta release of the feature. Tesla is preparing a wide rollout even as some of the Tesla loyalists testing the feature raise concerns about what will come next.
Some Tesla enthusiasts spoke out even before two people were killed in a Tesla over the weekend when it crashed into some trees. Police said that one occupant had been in the front passenger seat, and the other had been in one of the rear seats. There was no one in the driver's seat, the police said. The National Highway Traffic Safety Administration said Monday that is investigating the crash.
Two people died in a Tesla crash in Spring, Texas, over the weekend.
The police statement that there was no driver behind the wheel suggests that Autopilot, the widely available precursor to "full self-driving," may have been active and, if so, was being used inappropriately.
Tesla CEO Elon Musk said Monday that data logs recovered so far show Autopilot was not enabled. But Musk did not rule out that future findings could reveal Autopilot was in use. He also did not share an alternative theory for the crash.
Tesla did not respond to multiple requests for comment, and generally does not engage with the professional news media"""


# In[15]:


# res=""
# with open("new2.txt", "r") as fp:
#    line = fp.readline()
#    cnt = 1
#    while line:
#        res+=line+"."
#        #print("Line {}: {}".format(cnt, line.strip()))
#        line = fp.readline()
#        cnt += 1



# In[16]:


# returnSummary(res)


# In[ ]:


 
url = "https://edition.cnn.com/2021/05/10/politics/colonial-ransomware-attack-explainer/index.html" 
# download and parse article
article = Article(url)
article.download()
article.parse()
 

res = "".join([s for s in article.text.strip().splitlines(True) if s.strip("\r\n").strip()])
# print(res)
# res=""
# with article.text as fp:
#    line = fp.readline()
#    cnt = 1
#    while line:
#        res+=line+"."
#        #print("Line {}: {}".format(cnt, line.strip()))
#        line = fp.readline()
#        cnt += 1
print(returnSummary(res))

