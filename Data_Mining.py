
# coding: utf-8

# In[1]:

import sqlite3 as sq
import re
import pandas as pd
import os 

path=os.getcwd()
os.chdir(path)
#print os.getcwd()

## Getting the data through connecting with the new DB created for Data mining purposes only
conn = sq.connect("Wikipedia_Articles_DM.db")
cur = conn.cursor()


# In[2]:

###data frame for both featured and stub articles are created below 
### the data frame only contains all 22 attributes

def createDataFrame(table_name, label, art_ID):
    
    index = []
    rows = []
    
    for num_of_words, num_of_characters, num_of_images,avg_num_bytes,num_of_distinct_editors, num_edits,num_small_edits,num_IP_edits,     num_bot_edits, links_from, external_links, num_admin_edits, num_ref, num_ref_with_source, num_ref_no_source, num_ref_with_url,     num_ref_no_url, avg_edit_byte, age_in_days, currency_in_days, diversity,  admin_edit_share in     cur.execute('''Select num_of_words, num_of_characters, num_of_images,avg_num_bytes,num_of_distinct_editors, num_edits,num_small_edits,num_IP_edits,
    num_bot_edits, links_from, external_links, num_admin_edits, num_ref, num_ref_with_source, num_ref_no_source, num_ref_with_url,
    num_ref_no_url, avg_edit_byte, age_in_days, currency_in_days, diversity,  admin_edit_share from ''' +table_name):
        index.append(art_ID)
        rows.append({'number of words': num_of_words, 'number of characters':num_of_characters,'number of images':num_of_images, 'Average Size in Bytes':avg_num_bytes,                  'number of editors': num_of_distinct_editors, 'number of edits': num_edits, 'number of small edits': num_small_edits,                  'number of IP edits': num_IP_edits, 'number of bot edits': num_bot_edits, 'internal links': links_from, 'external links': external_links,                 'num_admin_edits': num_admin_edits,'num_ref': num_ref, 'num_ref_with_source':num_ref_with_source, 'num_ref_no_source':num_ref_no_source,                  'num_ref_with_url':num_ref_with_url, 'num_ref_no_url':num_ref_no_url, 'avg_edit_byte':avg_edit_byte, 'age_in_days':age_in_days,                  'currency_in_days':currency_in_days, 'diversity':diversity,  'admin_edit_share':admin_edit_share, 'label': label})         
                     
        art_ID += 1
    
    df = pd.DataFrame(rows, index=index)
    return df, art_ID


# In[3]:

df = pd.DataFrame({'number of words': [], 'number of characters':[], 'number of images':[], 'Average Size in Bytes':[], 'number of editors': [], 'number of edits': [], 'number of small edits': [], 'number of IP edits': [], 'number of bot edits': [], 'internal links': [], 'external links': [],  'num_admin_edits': [],'num_ref': [], 'num_ref_with_source':[], 'num_ref_no_source':[], 'num_ref_with_url':[], 'num_ref_no_url':[], 'avg_edit_byte':[], 'age_in_days':[], 'currency_in_days':[], 'diversity':[],  'admin_edit_share':[], 'label': []})

art_ID = 1

### create DataFrame for Feat
DF_f = createDataFrame("Featured_Data_Mining", "featured", art_ID)
f_df = DF_f[0]
art_ID = DF_f[1]
df = df.append(f_df)

### create DataFrame for Stub
DF_s = createDataFrame("Stub_Data_Mining", "stub", art_ID)
s_df = DF_s[0]
art_ID = DF_s[1]
df = df.append(s_df)


# In[4]:

###get rid off 'NaN' values by replacing them with 0

df.fillna(0, inplace=True)
#print df
#print df.iloc[:,[0,1,2,3,4,5,6,7,9,10,11,12,13,14,15,16,17,18,19,20,21,22]]
