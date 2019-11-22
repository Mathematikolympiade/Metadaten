<?php
/**
 * User: Hans-Gert Gräbe
 * Date: 2019-11-22
 * Last Update: 2019-11-22
 *
 */

require_once('lib/EasyRdf.php');
require_once('layout.php');

function Gebiete() {
  EasyRdf_Namespace::set('mo', 'https://www.mathematik-olympiaden.de/aufgaben/rdf/Model#');
  $graph = new EasyRdf_Graph("http://example.org/Graph/");
  $graph->parseFile("rdf/MO-Aufgaben.rdf");
  $res=$graph->allOfType('mo:Problem');
  $a=array();
  foreach ($res as $v) {
      $id=$v->get('mo:nr');
      foreach ($v->all('mo:zumGebiet') as $g) { // unklar, wie das mit mehrdimensionalen Arrays geht
          array_push($a[$g][],$id);
      }
  }
  print_r($a);
  $b=array();
  foreach($a as $v) {
      $b[]='<h3>Gebiet '.key($v).'</h3> <p>'.join(", ",$v).'</p>';
  }
  return join("\n",$b);
}

$content='
<div class="container">
<h2 align="center"> Klassifizierung nach Gebieten </h2>

<p>Diese Übersicht wurde aus den Metadaten der Aufgaben der AAG 9/10 und 11/13
extrahiert.</p> </div>
';

echo showPage($content.Gebiete());
