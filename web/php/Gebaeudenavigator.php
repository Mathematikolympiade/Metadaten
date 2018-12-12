<?php 

// --- Die main Funktion

function navigator() {  
  $out='<h3> Zur behindertengerechten Ausstattung Leipziger Orte </h3>';
  $out.=dieOrte();

  return $out;
}

function dieOrte() {
  $query = '
PREFIX bvlo: <https://github.com/AKSW/leds-asp-f-ontologies/raw/master/ontologies/place/ontology.ttl#>
SELECT *
FROM <https://opendata.leipzig.de/bvlplaces/>
WHERE {
?s a bvlo:Place; dc:title ?t .
}';
  
  $store = 'https://opendata.leipzig.de/virt-sparql';
  $r=queryStore($store,$query);
  // print_r($r);
  $out="<ul>\n";
  foreach ($r['results']['bindings'] as $k => $v) {
      $out.='<li><a href="getvirtdata.php?show='.$v['s']['value'].'">'.$v['t']['value']."</a></li>\n";
  }
  return $out."</ul>\n" ; 		
}
 
// ---- test ----
// echo navigator();