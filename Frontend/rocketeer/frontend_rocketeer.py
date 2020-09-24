import bottle
from bottle import get, post, route, request, run, abort, template, response, static_file, error
from collections import OrderedDict 
import string, operator
import database_creation as dbc
dbc.open_db()
import math
import sys

import sympy#ADD
from sympy import *#ADD

#current host IP
HOST_IP = "localhost:8080"
local = True
#HOST_IP = "ec2-204-236-205-78.compute-1.amazonaws.com"
if len(sys.argv) > 1:
    HOST_IP = sys.argv[1]
    local = False


keywords = OrderedDict() #ordered dictionary of all the words with count number in order
top_twenty_keywords = [] #list of tuples with words and their number of occurances
total_page_numbers=1

@get('/') #route of the search engine with GET
def search(): 

    #get the list of top 20 searches from all keywords in descending order based on value
    top_twenty_keywords = sorted(keywords.items(), key=operator.itemgetter(1),reverse=True)
	
    #template for the top 20 table
    top_twenty_table = template('Top_20_ListPrint', top_twenty_list=top_twenty_keywords, HOST_IP=HOST_IP)
   
	    
    words_dict = request.query 

    #search request is in url or nothing or just space is entered, run search request page	  
    if 'keywords' in words_dict.keys() and len(words_dict['keywords']) != 0 and (words_dict['keywords'].isspace()!= True): 

        all_words = words_dict['keywords']
        
        words = str(all_words.lower()).split() #separate all the words and in lower case
	
        search=dbc.get_results_for_multi_word(words)#search is list of results
	
	#if no result is found return the page to inform user
        if search is None:
            search_NotFound=template('No_results',HOST_IP=HOST_IP,searchword=' '.join(words))
            return search_NotFound

        current_words = [] #list of the words searched each time
        word_counts = {} #dictionary of words and their number of occurances each time
        
        #for every word, loops through and count the number of occurances
        for word in words:
          
            if word in current_words:
                word_counts[word] += 1
            else:
                current_words.append(word)
                word_counts[word] = 1
           
        new_keywords = [] #list of tuples with words and number of occurances in order
  
        #loop through and update the number of occurances for each words in total 
        for word in current_words:
            new_keywords.append((word, word_counts[word]))
            if word in keywords:
                keywords[word] += word_counts[word]
            else:
                keywords[word] = word_counts[word]

        #redirect the url to page 1 if results found
        bottle.redirect("http://" + HOST_IP + "/search/" + str("+".join(words)) + "/1")
        
    else: #no search request in url, run main page

        #return the top 20 table on the main page
        return top_twenty_table

@route('/search/<search_words>/<page_num:int>')
def pag(search_words, page_num=1):
    
    results_per_page=5
    words = search_words.split('+')
    title_word = (' '.join(words))

    search=dbc.get_results_for_multi_word(words)#search is list of results
    
    #index limits of the links shown per page
    first_page = (page_num -1)* 5 
    last_page = min(page_num* 5, len(search) - 1)
    
    results_for_page = search[(page_num -1)* 5 : (page_num)* 5];
    
    this_url = "http://" + HOST_IP + "/search/" + search_words + "/"
     
    #total page numbers needed to show all search results
    total_page_numbers=len(search)/5
    if(len(search) % 5 != 0):
        total_page_numbers = total_page_numbers + 1
    
    #return the resulting page
    search_result=template('search_results', total_page_numbersa=total_page_numbers, len_a=len(search),searcha=results_for_page, searchword=words, title=title_word, page_num=page_num, page_url=this_url, next_page = min(page_num + 1,total_page_numbers) , prev_page = max(page_num - 1, 1), HOST_IP=HOST_IP)

    return search_result

    
@error(404)
def error404(error):
    #show error page and give link for search engine if invalid url entered
    ErrorPage = template('error_link',HOST_IP=HOST_IP)
    return 'Nothing here, sorry', ErrorPage

@route('/calculator')
def calculator():
    calculator_input = request.query 
    #search request is in url or nothing or just space is entered, run search request page	  
    if 'cal' in calculator_input.keys() and len(calculator_input['cal']) != 0 and (calculator_input['cal'].isspace()!= True): 
        
        calculator_query = calculator_input['cal']
        try: 
            calculator_result= sympify(calculator_query)
        except: 
            calculator_result= "invalid input"
            

    calculator_page=template('calculator', HOST_IP=HOST_IP,calculator_querya=calculator_query, calculator_resulta=calculator_result)
    return calculator_page

@route('/static/rocketeer.gif')
def logo():
    return static_file('rocketeer.gif', root='static/')


if local:
    run(host='localhost', port=8080, debug=True)
else:
    run(host='0.0.0.0',   port=80,   debug=True, reloader=True)
