
# coding: utf-8

# In[34]:

import sqlite3
import re
import pandas as pd

conn = sqlite3.connect("Wikipedia_Articles.db")
cur = conn.cursor()


# In[41]:

########## OG
def createDataFrame(table_name, label, art_ID):
    
    index = []
    rows = []
    
    for name, main_text in cur.execute('''Select name, main_text from '''+table_name):
        index.append(art_ID)
        rows.append({'name': name, 'main_text': main_text, 'label': label})
        art_ID += 1
    
    df = pd.DataFrame(rows, index=index)
    return df, art_ID


# In[42]:

df = pd.DataFrame({'name': [], 'main_text': [], 'label': []})

art_ID = 1

### create DataFrame for Feat
DF_f = createDataFrame("Featured_Articles", "featured", art_ID)
f_df = DF_f[0]
art_ID = DF_f[1]
df = df.append(f_df)

### create DataFrame for Stub
DF_s = createDataFrame("Stub_Articles", "stub", art_ID)
s_df = DF_s[0]
art_ID = DF_s[1]
df = df.append(s_df)


# In[43]:

from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier

from sklearn.cross_validation import cross_val_score
from sklearn.cross_validation import KFold
from sklearn.cross_validation import StratifiedKFold
from sklearn.metrics import confusion_matrix, f1_score
from sklearn.metrics import accuracy_score


# In[44]:

from sklearn.feature_extraction.text import CountVectorizer 
cVect = CountVectorizer(token_pattern='(?u)\\b\\w+\\b')
countTbyD = cVect.fit_transform(df['main_text'].values) 

from sklearn.feature_extraction.text import TfidfVectorizer
tfidfVect = TfidfVectorizer(token_pattern='(?u)\\b\\w+\\b')
tfidfTbyD = tfidfVect.fit_transform(df['main_text'].values)
