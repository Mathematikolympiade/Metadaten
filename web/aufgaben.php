<?php
/**
 * User: Hans-Gert Gräbe
 * Date: 2017-09-04 
 * Last Update: 2018-12-12
 *
 */

function listeAufgaben($store) {
    $query='
PREFIX ksn: <http://kosemnet.de/Data/Model#> 
select ?u ?g ?s
from <http://kosemnet.de/Data/MO-Aufgaben/>
where {
 ?a a ksn:AufgabenVorschlag; owl:sameAs ?u . 
 optional { ?a ksn:zumGebiet ?g . }
 optional { ?a ksn:hatSchwierigkeit ?s . }
} order by ?u
';
    $r=queryStore($store,$query);
    $a=array();
    foreach ($r['results']['bindings'] as $k => $v) {
        $nr=str_replace("http://kosemnet.de/Data/Aufgabe/","",$v['u']['value']);
        $a[]='<tr><td>'.$nr.'</td> <td>'.$v['g']['value']
            .'</td> <td>'.$v['s']['value'].'</td> </tr>';
    }
    return '
<table align="center" width="80%"> 
<tr> <th> Aufgabe </th> <th> Gebiet </th> <th> Schwierigkeit </th> </tr>'.
    join("\n",$a).'</table>';
}

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

echo listeAufgaben('http://pcai003.informatik.uni-leipzig.de:8893/sparql');
