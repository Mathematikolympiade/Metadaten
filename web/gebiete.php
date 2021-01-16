<?php
/**
 * User: Hans-Gert Gräbe
 * Last Update: 2019-11-22
 *
 */

require_once('lib/EasyRdf.php');
require_once('layout.php');

function Gebiete() {
  EasyRdf_Namespace::set('mo', 'https://www.mathematik-olympiaden.de/aufgaben/rdf/Model#');
  $graph = new EasyRdf_Graph("http://example.org/Graph/");
  $graph->parseFile("rdf/MO-Basisdaten.rdf");
  $graph->parseFile("rdf/MO-AufgabenNachGebieten.rdf");
  $res=$graph->allOfType('mo:Problem');
  $a=array();
  foreach ($res as $v) {
      $id=$v->get('mo:nr');
      foreach ($v->all('mo:zumGebiet') as $g) { 
          if (!(is_array($a["$g"]))) { $a["$g"]=array(); }
          array_push($a["$g"],"$id");
      }
  }
  // print_r($a);
  $b=array();
  foreach($a as $k => $v) {
      $b[]='<h3>Gebiet '.$k.'</h3> <p>'.join(", ",$v).'</p>';
  }
  return '<div class="container">'.join("\n",$b).'</div>';
}

$content='
<div class="container">
<h2 align="center"> Klassifizierung nach Gebieten </h2>

<p>Diese Übersicht wurde aus den Metadaten der Aufgaben der AAG 9/10 und 11/13
extrahiert.</p> </div>
';

echo showPage($content.Gebiete());
