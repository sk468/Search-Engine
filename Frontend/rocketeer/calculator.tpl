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
th, td{
    padding:5px;
}
td{
    text-align:center;
}
p{
    color:black;
    font-family:garamond;
   
}
body{
    font-family:garamond;
    background-color:powderblue;
    text-align:center;
    font-size:20pt;
    font-family:garamond;
}
#keywords{
    height:50px;
    width:600px;
    font-size:20pt;
}
#cal{
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
    font-size:45pt;
}
#search_URL{
    color:green;
    font-family:garamond;
    font-size:30pt;
}
#search_Description{
    color:grey;
    font-family:garamond;
    font-size:20pt;
}
#search_Title:link{
    color:green; 
    background-color:transparent; 
    text-decoration:none;    
}
#search_Title:visited{
    color:pink; 
    background-color:transparent; 
    text-decoration:none;  
}
#search_Title:hover{
    color:orange; 
    background-color:transparent; 
    text-decoration:none;  
}
#search_Title:active{
    color:yellow; 
    background-color:transparent; 
    text-decoration:none;  
}
#calculatebutton{
    height:57px;
    width:200px;
    font-size:20pt;
    border-radius:8px;
    background-color:#B2DFFF; 
    border:2px solid #006BCD;
}
#calculatebutton:hover{
    background-color:#006BCD;
    color:white;
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
<body>
<img src="http://{{HOST_IP}}/static/rocketeer.gif" width="540" height="340" style="text-align:center;"/>
<form action="/" method="get"> <input id="button_to_homepage"value="Back to Homepage" type="submit" /> </form>
<br></br>
<!--form and button for search bar-->
<form action="/" method="get"> &nbsp &nbsp Search: <input id="keywords" name="keywords" type="text" /> <input id="button1"value="Submit" type="submit" /> </form>
<br></br>
<form action="/calculator" method="get"> Calculate: <input id="cal" name="cal" type="text" /> <input id="calculatebutton"value="Calculate" type="submit" /> </form>
<br></br>
<b><p style="text-align:left;">  {{calculator_querya}} = {{calculator_resulta}}</p></b>



</body>
</html>
