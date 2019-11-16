<?php 

require_once("lib/EasyRdf.php");

function queryStore($store,$query) {
    $get_parameters =
        '?query=' . urlencode ($query) .
        '&format=application%2Fsparql-results%2Bjson' ; 
    $req = $store . $get_parameters;
    $result = file_get_contents($req);
    //print_r($result);
    $r = json_decode($result,true);
    //print_r($r);
    return $r;
}


function wrap($u) {
    if ($u['type']=="uri") return '<'.$u['value'].'>';
    else return '"'.$u['value'].'"';
}

function prettyprint($u) {
    return "<pre>".htmlspecialchars($u)."</pre>";
}

function zdtrim($s) {
    return str_replace("http://leipzig-data.de/Data/",'',$s);
}

function mehrzeilig($s) {
    return str_replace("\n",'<br/>',$s);
}

function fixListe($a) {
    $b=array(); 
    foreach($a as $event) {
        $b[]='<li> '.str_replace("\n",'<br/>',$event).' </li>' ;
    }
    return "<ul>".join("\n",$b)."</ul>";
}

function showURL($url) {
    return '<a href="'.$url.'">'.$url.'</a>';
}
