import urllib2
import re
from bs4 import BeautifulSoup

####### TESTING CLEANING
import nltk
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
####### TESTING CLEANING
stop_words = stopwords.words('english')
lmtzr = WordNetLemmatizer()
####### TESTING CLEANING

def getArticleData(url, headers):
    req = urllib2.Request(url, None, headers)
    response = urllib2.urlopen(req).read()
    tree = BeautifulSoup(response,"html.parser")
    title = tree.findAll('h1',{'id': 'firstHeading'})[0].text
    main_text = tree.findAll('div',{'id': 'mw-content-text'})[0].text
    
    ####### TESTING CLEANING
    temp_text_list = []
    ####### TESTING CLEANING
    
    try:
        main_text = main.rsplit("Bibliography",1)[0]
        main_text = main.rsplit("References",1)[0]
        main_text = main.rsplit("Notes",1)[0]
    except Exception: 
    	pass
    main_text = re.sub('\s+',' ', main_text)
    main_text = re.sub(r'[^\w\s]',' ', main_text)
    
    ####### TESTING CLEANING
    for words in main_text.split():
    	if words not in stop_words:
    		lem_words = lmtzr.lemmatize(words)
    		temp_text_list.append(lem_words)
    	main_text = " ".join(temp_text_list)
    ####### TESTING CLEANING
    
    main_text_words = len(main_text.split())
    main_text_chars = len(main_text) - main_text.count(' ')
    imgs = len(tree.findAll(['img', 'src']))
          
    return title, main_text, main_text_words, main_text_chars, imgs

def getRefsData(url, headers):
    tags_article_refs = []; 
    req = urllib2.Request(url, None, headers)
    response = urllib2.urlopen(req).read()
    tree = BeautifulSoup(response,"html.parser")
    references = tree.findAll('span',{'class': 'reference-text'})
    for tag in references:
        tags_article_refs.append(tag)
    
    name_ref = []; url_ref = []; source_ref = [];
    for ref in tags_article_refs:
        ## Retrieving the name of the ref
        name_ref.append(ref.text)
        ## Retrieving a possible url of the ref, else no url is added
        try:
            url = ref.findAll('a', href=True)[0].get('href')
            url_ref.append(url)
        except:
            url_ref.append('No url')
        ## Retrieving a possible source of the ref, else no direct source is added
        try:
            source = ref.findAll('i')[0].text
            source_ref.append(source)
        except:
            source_ref.append('No source')
    
    num_refs = len(name_ref)
    
    return name_ref, url_ref, source_ref, num_refs

def getStatisticsData(title, headers):
    statistics_url = "https://tools.wmflabs.org/xtools-articleinfo/?article="+title.replace(" ","_")+"&project=en.wikipedia.org&editorlimit=300&editorlimit=10000#topeditors"
    req = urllib2.Request(statistics_url, None, headers)
    response = urllib2.urlopen(req).read()
    tree = BeautifulSoup(response,"html.parser")
    statistics = tree.findAll('div',{'id': 'generalstats'})
    for tags in statistics:
        ## Table 1
        table_stats = tags.findAll('td',{'class': 'tdtop1'})
        versions = int(table_stats[3].text.replace(",",""))
        num_edits = int(table_stats[4].text.replace(",",""))
        num_small_edits = int(table_stats[5].text.split(" ",1)[0].replace(",",""))   ## split method is used, beaucse it contains non usable information
        num_ip_edits = int(table_stats[6].text.split(" ",1)[0].replace(",","")) 
        num_bot_edits = int(table_stats[7].text.split(" ",1)[0].replace(",","")) 
        date_first_edit = table_stats[17].findAll('span')[0].text
        first_editor = table_stats[17].findAll('a')[0].text
        date_last_edit = table_stats[18].findAll('span')[0].text
        latest_editor = table_stats[18].findAll('a')[0].text
        ## Table 2
        table_stats2 = tags.findAll('span',{'class': 'tdgeneral'})
        links_from_article = int(table_stats2[2].text.replace(",","")) 
        external_links = int(table_stats2[3].text.replace(",",""))
	   
    return versions , num_edits, num_small_edits, num_ip_edits, num_bot_edits, date_first_edit, first_editor, date_last_edit, latest_editor, links_from_article, external_links, statistics_url, links_from_article, external_links

def getEditorStatistics(statistics_url,headers):
    req = urllib2.Request(statistics_url, None, headers)
    response = urllib2.urlopen(req).read()
    tree = BeautifulSoup(response,"html.parser")
    editors = tree.findAll('table',{'class': 'sortable table-striped table-condensed xt-table'})[0].contents
    
    editor_names = []; editor_pages = []; number_edits_editors = []; number_minor_edits_editors = []; 
    first_edits = []; last_edits = []; average_time_between_edits = []; bytes_added_article_editors = []; 
    
    bytes_article_sum = 0
    distinct_users_temp = [];
    
    for edits in editors[3:len(editors):2]:
        editor_name = edits.findAll("td")[0].text; 
        editor_names.append(editor_name)
        
        if editor_name not in distinct_users_temp:
        	distinct_users_temp.append(editor_name)
        
        editor_page = edits.findAll("td")[0].findAll('a', href=True)[0].get('href').replace("//","https://"); 
        editor_pages.append(editor_page)
        number_edits = int(edits.findAll("td")[2].text.replace(",","")) 
        number_edits_editors.append(number_edits)
        number_minor_edits = int(edits.findAll("td")[3].text.replace(",",""))
        number_minor_edits_editors.append(number_minor_edits)
        first_edit = edits.findAll("td")[5].text 
        first_edits.append(first_edit)
        last_edit = edits.findAll("td")[6].text 
        last_edits.append(last_edit)
        avg_time_btw_edits = edits.findAll("td")[7].text; 
        average_time_between_edits.append(avg_time_btw_edits)
        bytes_add_edit = int(edits.findAll("td")[8].text.replace(",","")) 
        bytes_added_article_editors.append(bytes_add_edit)
        
        bytes_article_sum = bytes_article_sum + bytes_add_edit
    avg_bytes_added = bytes_article_sum / len(editors[3:len(editors):2])
    number_distinct_users = len(distinct_users_temp)
    
    return  editor_names, editor_pages, number_edits_editors, number_minor_edits_editors, first_edits, last_edits, average_time_between_edits, bytes_added_article_editors, avg_bytes_added, number_distinct_users 
    