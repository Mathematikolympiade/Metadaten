<?php
/**
 * User: Hans-Gert Gräbe
 * Last Update: 2021-01-16
 *
 */

require_once('lib/EasyRdf.php');
require_once('layout.php');

function AufgabenVorschlaege() {
  EasyRdf_Namespace::set('mo', 'https://www.mathematik-olympiaden.de/aufgaben/rdf/Model#');
  $graph = new EasyRdf_Graph("http://example.org/Graph/");
  $graph->parseFile("rdf/AAG9-Intern.rdf");
  $graph->parseFile("rdf/MO-Basisdaten.rdf");
  $res=$graph->allOfType('mo:AufgabenVorschlag');
  $a=array();
  foreach ($res as $v) {
      $id=str_replace('https://www.mathematik-olympiaden.de/aufgaben/rdf/AufgabenVorschlag/','',$v->getURI());
      $gebiet=join(", ",$v->all('mo:zumGebiet'));
      $schwierigkeit=join(", ",$v->all('mo:hatSchwierigkeit'));
      if ($v->get("owl:sameAs")) { $mo=$v->get("owl:sameAs")->get("mo:nr"); }
      $a[]='<tr align="center"><td>'.$id.'</td> <td>'.$schwierigkeit.'</td> <td>'.$gebiet.'</td> <td>'
          .$mo.'</td> </tr>';
    }
    return '
<div class="container">
<table align="center" border="1"> 
<tr align="center"> <th> Aufgabe </th> <th> Schwierigkeit </th> <th> Gebiet </th> <th> MO-Aufgabe </th>  </tr>'.
    join("\n",$a).'</table></div>';
}

$content='
<div class="container">
<h2 align="center"> Klassifizierung von Aufgabenvorschlägen </h2>

<p>Diese Übersicht wurde aus den Metadaten der Aufgaben der AAG 9/10
extrahiert.</p>
</div>
';

echo showPage($content.AufgabenVorschlaege());
