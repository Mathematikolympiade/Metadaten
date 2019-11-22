<?php
/**
 * User: Hans-Gert Gräbe
 * Date: 2017-09-04 
 * Last Update: 2019-11-16
 *
 */

require_once('lib/EasyRdf.php');
require_once('layout.php');

function Aufgaben() {
  EasyRdf_Namespace::set('mo', 'https://www.mathematik-olympiaden.de/aufgaben/rdf/Model#');
  $graph = new EasyRdf_Graph("http://example.org/Graph/");
  $graph->parseFile("rdf/MO-Aufgaben.rdf");
  $res=$graph->allOfType('mo:Problem');
  $a=array();
  foreach ($res as $v) {
      $id=$v->get('mo:nr');
      $gebiet=join(", ",$v->all('mo:zumGebiet'));
      $schwierigkeit=join(", ",$v->all('mo:hatSchwierigkeit'));
      $a[]='<tr><td>'.$id.'</td> <td align="center">'.$schwierigkeit
          .'</td> <td>'.$gebiet.'</td> </tr>';
    }
    return '
<div class="container">
<table align="center" border="1"> 
<tr> <th> Aufgabe </th> <th> Schwierigkeit </th> <th> Gebiet </th> </tr>'.
    join("\n",$a).'</table></div>';
}

$content='
<div class="container">
<h2 align="center"> Klassifizierung von Aufgaben </h2>

<p>Diese Übersicht wurde aus den Metadaten der Aufgaben der AAG 9/10
extrahiert.</p>
</div>
';

echo showPage($content.Aufgaben());
