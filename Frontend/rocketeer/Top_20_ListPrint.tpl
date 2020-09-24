
<!DOCTYPE html>
<html>
<head><title>Rocketeer Search Engine</title>

<!--classes for characteristics/style of each part (paragraphs, tables, buttons etc.)-->
<style>
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

#cal{
    height:50px;
    width:600px;
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

</style>
</head>

<!--getting the image from source with specified style-->
<body>
<img src="http://{{HOST_IP}}/static/rocketeer.gif" width="540" height="340" style="text-align:center;"/> 

<!--form and button for search bar-->
<form action="/" method="get"> &nbsp &nbsp Search: <input id="keywords" name="keywords" type="text" /> <input id="button1"value=" Submit " type="submit" /> </form>
<br></br>
<form action="/calculator" method="get"> Calculate: <input id="cal" name="cal" type="text" /> <input id="calculatebutton"value="Calculate" type="submit" /> </form>
<p style="text-align:left;"> Top 20 Most Popular Keywords:</p>

<!--table for top 20 most searched words-->
<table>
<table id=“history” style="width:25%">
<tr><th>Word</th>
<th>Count</th></tr>
%for word, freq in top_twenty_list[0:20]:
	   <tr>
		   <td> {{word}} </td>
		   <td> {{freq}} </td>
	   </tr>
%end
</table>
</body>
</html>
