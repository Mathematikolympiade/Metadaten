<?php 

require_once("lib/EasyRdf.php");

function trans() {
  EasyRdf_Namespace::set('mo', 'https://www.mathematik-olympiaden.de/aufgaben/rdf/Model#');
  $graph = new EasyRdf_Graph("http://example.org/Graph/");
  $graph->parseFile("../rdf/AAG9-Intern.rdf");
  $res=$graph->allOfType('mo:AufgabenVorschlag');
  $out='';
  foreach ($res as $a) {
      $id=str_replace('https://www.mathematik-olympiaden.de/aufgaben/rdf/AufgabenVorschlag/','',$a->getURI());
      $gebiete=join(", ",$a->all('mo:zumGebiet'));
      $out.="$id:\t $gebiete\n";
  }
  return $out;

}

echo trans();
