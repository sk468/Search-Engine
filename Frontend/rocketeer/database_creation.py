import sqlite3 as sql

conn = None
c = None


#open the database
def open_db():
    global conn 
    conn = sql.connect('rocketeer.db')
    global c 
    c = conn.cursor()

#close the database
def close_db():
    conn.close()
    
#get search results for a single word, run after open_db()
def get_results_for_word(word):
    if not isinstance(word,str):
        print "Error: word being searched for is not a string"
        return None
    
    c.execute("SELECT doc_ids FROM words WHERE word=?", (word, ))
    word_docs = c.fetchone()
    if word_docs == None:
        return None
    docs_weights = map(int, word_docs[0].split())
    weights = []
    word_docs = []
    for i in range(0, len(docs_weights)):
        if i % 2 == 0:
            word_docs.append(docs_weights[i])
        else:
            weights.append(docs_weights[i])
    
    search_for = " OR id=".join(map(str, word_docs))
    search_command = 'SELECT * FROM docs WHERE id=%s ORDER BY pagerank DESC'% (search_for, )
    c.execute(search_command)
    docs_tuples = c.fetchall()
    docs = []
    i = 0
    
    for doc in docs_tuples:
        docs.append(list(doc))
        weight = weights[word_docs.index(docs[i][0])] #find corresponding weight for doc id
        
        docs[i][-1] *= weight #scale the pagerank by the words weight on the page
        
        i += 1
    
    docs.sort(key=lambda x: x[-1], reverse = True)
    
    return docs

#get results for a list/tuple of words, run after open_db()
def get_results_for_multi_word(words):
    docs = dict()
    
    for word in words:
        c.execute("SELECT doc_ids FROM words WHERE word=?", (word, ))
        word_docs = c.fetchone()
        if word_docs == None:
            continue
        docs_weights = map(int, word_docs[0].split())
        weights = []
        word_docs = []
        for i in range(0, len(docs_weights)):
            if i % 2 == 0:
                word_docs.append(docs_weights[i])
            else:
                weights.append(docs_weights[i])

        search_for = " OR id=".join(map(str, word_docs))
        search_command = 'SELECT * FROM docs WHERE id=%s ORDER BY pagerank DESC'% (search_for, )
        c.execute(search_command)
        docs_tuples = c.fetchall()

        for doc in docs_tuples:
            tmp = list(doc)
            weight = weights[word_docs.index(tmp[0])] #find corresponding weight for doc id

            tmp[-1] *= weight #scale the pagerank by the words weight on the page
            
            if tmp[0] in docs.keys():
                docs[tmp[0]][-1] += tmp[-1]
            else:
                docs[tmp[0]] = list(tmp)
    
    
    full_list = docs.values()
    full_list.sort(key=lambda x: x[-1], reverse = True)
    
    return full_list
    
    
    
#c.execute('SELECT * FROM docs WHERE id=1 OR id=3 OR id=2 ORDER BY pagerank DESC')
