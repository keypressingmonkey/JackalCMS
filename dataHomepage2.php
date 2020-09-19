<?php
//ajax call sends page parameter via GET
$page = $_GET["page"];

//pageSize = number of elements to display (because I use a static json this param is ignored but when calling DB you have there page and limit)
$pageSize = $_GET["pageSize"];

//get from DB the total number of pages (right now is static)
$totalPages = 3;

//this should be replaced with data from DB
//somethign like $data = mysql_query("SELECT * FROM friends LIMIT $page, $page * $pageSize ");
$string = file_get_contents("json/homepage2-page".$page.".json");

//ignore this, it's only for static json
$json_a=json_decode($string,true);

//this is required to have the totalPages in the return of the call
$json_a['totalPages'] = 3;

//return the data from DB in json format
echo json_encode($json_a);