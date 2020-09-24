The test script run_backend_test.py can be run to run a simple backend test.

Before running the test you must ensure that any preexisting rocketeer.db file is removed from the folder in which you are running the script. 

The script will crawl the urls in test-urls.txt (currently eecg.toronto.edu) to a depth of one, will compute the pagerank of the pages found, and will store the results in a sqlite database. It will then open the database, retrieve the pages found, and will print the title and pagerank score of each page in descending order by pagerank. 