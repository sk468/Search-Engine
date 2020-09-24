import sqlite3 as sql
import crawler

conn = None
c = None

def setup_db(id_word_cache, inverted_index, documents, doc_word_weight):
    """Function takes a mapping of word id's to actual words,
        an inverted index of word id's to document id's containing the words
        and a dictionary mapping from document id's to document info
        
        The function creates two tables, 
        The first table, 'words' contains two columns
        1. 'word' that is the word being looked for
        2. 'doc_ids' which is a space-separated string of document id's containing the word
        The second table, 'docs' contains 5 columns
        1. 'id' document id
        2. 'title' the document title
        3. 'url' the document url
        4. 'summary' the document summary if it exists
        5. 'pagerank' the document's pagerank"""
    
    conn = sql.connect('rocketeer.db')
    c = conn.cursor()
    
    #make the tables
    c.execute('''CREATE TABLE words
             (word text, doc_ids text)''')
    c.execute('''CREATE TABLE docs
             (id integer, title text, url text, summary text, pagerank real)''')
    
    word_table = []
    for word_id in inverted_index:
        curr_word = id_word_cache[word_id]
        docs_weights = []
        for doc in inverted_index[word_id]:
            docs_weights.append(doc)
            docs_weights.append(doc_word_weight[(doc, word_id)])
        
        ids_string = " ".join(map(str,docs_weights))
        word_table.append((curr_word, ids_string))
        
    db_documents = []
    for doc_id in documents:
        doc_info = documents[doc_id]
        db_documents.append((doc_id, doc_info.title, doc_info.url, doc_info.summary, doc_info.pagerank))
        
    c.executemany('INSERT INTO words VALUES (?,?)', word_table)
    c.executemany('INSERT INTO docs VALUES (?,?,?,?,?)', db_documents)
    conn.commit()
    conn.close()
    
    
    
def test_db():
    id_word_cache = {0:'hello', 1:'butwhy', 2:'ineedabreak'}
    inverted_index  = {0:set([1, 2]), 1:set([3]), 2:set([1, 3])}
    documents = {1:crawler.document(), 2:crawler.document(), 3:crawler.document()}
    documents[1].url = "www.google.com"
    documents[1].summary = "search engine"
    documents[1].title = "google"
    documents[1].pagerank = 0.05
    documents[2].url = "www.bing.com"
    documents[2].summary = "bing search engine"
    documents[2].title = "bing"
    documents[2].pagerank = 0.03
    documents[3].url = "www.wikipedia.com"
    documents[3].summary = "online encyclopedia"
    documents[3].title = "wikipedia"
    documents[3].pagerank = 0.06
    
    doc_word_weight = {(1,0):5, (2,0):8, (3,1):2, (1,2):4, (3,2):9}
    
    setup_db(id_word_cache, inverted_index, documents, doc_word_weight)
    
def open_db():
    global conn 
    conn = sql.connect('rocketeer.db')
    global c 
    c = conn.cursor()
    
def close_db():
    conn.close()
    
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