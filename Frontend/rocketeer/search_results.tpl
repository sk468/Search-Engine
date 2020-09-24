<!DOCTYPE html>
<html>
<head><title>Rocketeer Search Engine</title>

<!--classes for characteristics/style of each part (paragraphs, tables, buttons etc.)-->
<style>


.pagination {
    display: inline-block;
    font-size:20pt;
    text-align:center;
}

.pagination a {
    color: black;
    float: left;
    padding: 8px 16px;
    text-decoration: none;
    font-size:20pt;
    text-align:center;
}

.pagination a.active {
    background-color: #4CAF50;
    color: white;
    font-size:20pt;
    text-align:center;
}

.pagination a:hover:not(.active) {background-color: #ddd;}
table, th, td{
    font-family:garamond;
    font-size:20pt;
    border-collapse:collapse; 
}

table, th, td{
    font-family:garamond;
    font-size:20pt;
    border-collapse:collapse; 
}
th, td{
    padding:5px;
}
td{
    text-align:center;
}
p{
    color:grey;
    font-family:garamond;
   
}
body{
    font-family:garamond;
    background-color:powderblue;
    text-align:center;
    font-size:20pt;
}
#keywords{
    height:50px;
    width:600px;
    font-size:20pt;
}
#button1{
    height:57px;
    width:200px;
    font-size:20pt;
    border-radius:8px;
    background-color:#B2DFFF; 
    border:2px solid #006BCD;
}
#button1:hover{
    background-color:#006BCD;
    color:white;
}
#search_Title{
    color:blue;
    font-family:garamond;
    font-size:20pt;
}
#search_URL{
    color:maroon;
    font-family:garamond;
    font-size:15pt;
}
#search_Description{
    color:grey;
    font-family:garamond;
    font-size:15pt;
}
#search_Title:link{
    color:blue; 
    background-color:transparent; 
    text-decoration:none;    
}
#search_Title:visited{
    color:red; 
    background-color:transparent; 
    text-decoration:none;  
}
#search_Title:hover{
    color:salmon; 
    background-color:transparent; 
    text-decoration:none;  
}
#search_Title:active{
    color:yellow; 
    background-color:transparent; 
    text-decoration:none;  
}
#button_to_homepage{
    height:57px;
    width:500px;
    font-size:20pt;
    border-radius:8px;
    background-color:#B2DFFF; 
    border:2px solid #006BCD;
}
#button_to_homepage:hover{
    background-color:#006BCD;
    color:white;
}

</style>
</head>

<!--getting the image from source with specified style-->
<body>
<img src="http://{{HOST_IP}}/static/rocketeer.gif" width="540" height="340" style="text-align:center;"/> 
<form action="/" method="get"> <input id="button_to_homepage"value="Back to Homepage" type="submit" /> </form>
<br></br>
<!--form and button for search bar-->
<form action="/" method="get"> Search: <input id="keywords" name="keywords" type="text" /> <input id="button1"value="Submit" type="submit" /> </form>

<!--show results found for corresponding search--> 
<body>
<p style="text-align:left;">{{len_a}} Search Results for '{{title}}':</p>

<ul style="list-style-type:disc">
%for index in searcha:
	%pass
	<a href="{{index[2]}}" style="text-align:left;" target="_blank"><p id="search_Title"> <li> 
    %if index[1]:
<!--bold title words if they are one of the search terms--> 
        %for word in index[1].split():
            %if word.lower() in searchword:
            <b>{{word + ' '}}</b>
        %end
            %if not word.lower() in searchword:
            {{word + ' '}}
            %end
        %end
    %end
    </li></p></a>
    	<p id="search_URL" style="text-align:left;">{{index[2]}}</p>
    	<p id="search_Description" style="text-align:left;">\\
<!--bold summary words if they are one of the search terms--> 
            %if index[3]:
            %for word in index[3].split():
            %if word.lower() in searchword:
            <b>{{word + ' '}}</b>
            %end
            %if not word.lower() in searchword:
            {{word + ' '}}
            %end
            %end
            %end
    </p>
	<p></p>
%end
</ul>
</body>

<!--pagination-->

<div class="pagination" align=center style="text-align:center;">
  	<a href={{page_url}}{{prev_page}}>&laquo; Previous</a>
	%for i in range(1,total_page_numbersa+1):
  		<a href={{page_url}}{{i}}>{{i}}</a>
	%end
  		<a href={{page_url}}{{next_page}}>Next &raquo;</a>
</div>

</body>
</html>
