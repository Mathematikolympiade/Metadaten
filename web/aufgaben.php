<?php
/**
 * User: Hans-Gert Gräbe
 * Last Update: 2019-11-22
 *
 */

require_once('lib/EasyRdf.php');
require_once('layout.php');

function Aufgaben() {
  EasyRdf_Namespace::set('mo', 'https://www.mathematik-olympiaden.de/aufgaben/rdf/Model#');
  EasyRdf_Namespace::set('mop', 'https://www.mathematik-olympiaden.de/aufgaben/rdf/Aufgabe/');
  $graph = new EasyRdf_Graph("http://example.org/Graph/");
  $graph->parseFile("rdf/MO-Basisdaten.rdf");
  $graph->parseFile("rdf/MO-AufgabenNachGebieten.rdf");
  $res=$graph->allOfType('mo:Problem');
  $a=array();
  foreach ($res as $v) {
      $id=$v->get('mo:nr');
      // if (empty($id)) { echo $v->dump("text") ; }
      $gebiet=join(", ",$v->all('mo:zumGebiet'));
      if ($gebiet) {
          $a["$id"]='<tr align="center"><td>'.$id.'</td> <td>'.$gebiet.'</td> </tr>';
      }
  }
  ksort($a);
  return '
<div class="container">
<table align="center" border="1"> 
<tr align="center"> <th> Aufgabe </th> <th> Gebiet </th>  </tr>'.
    join("\n",$a).'</table></div>';
}

$content='
<div class="container">
<h2 align="center"> Klassifizierung von Aufgaben </h2>

<p>Diese Übersicht wurde aus den Metadaten der Aufgaben der AAG 9/10 und 11/13
extrahiert.  Es sind nur diejenigen Aufgabennummern gelistet, zu denen eine
Gebietsinformation vorhanden ist. </p> </div>
';

echo showPage($content.Aufgaben());
