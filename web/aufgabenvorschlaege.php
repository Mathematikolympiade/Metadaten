<?php
/**
 * User: Hans-Gert Gräbe
 * Last Update: 2021-01-17
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
      $status=$v->get('mo:hatStatus');
      if ($v->all("owl:sameAs")) {
          $b=array();
          foreach ($v->all("owl:sameAs") as $mo) {
              if ($mo->get("mo:nr")) { $b[]=$mo->get("mo:nr"); }
          }
          $status=join(", ",$b);
      }
      $a[]='<tr align="center"><td width="20%">'.$id.'</td> <td>'.$schwierigkeit.'</td> <td>'
          .$gebiet.'</td> <td>'.$status.'</td> </tr>';
    }
    return '
<div class="container">
<table class="table table-bordered table-hover w-75" align="center" style="margin-top:3em"> 
<thead>
  <tr> 
   <th scope="col" class="text-center"> Aufgabe </th> 
   <th scope="col" class="text-center"> Schwierigkeit </th> 
   <th scope="col" class="text-center"> Gebiet </th> 
   <th scope="col" class="text-center"> Status </th>  
  </tr>
</thead>
<tbody>'.
    join("\n",$a).'</tbody></table></div>';
}

$content='
<div class="container">
<h2 align="center"> Klassifizierung von Aufgabenvorschlägen </h2>

<p>Hier nun eine etwas umfassendere Übersicht der Aufgaben der AAG 9/10, die
aus den Metadaten der Aufgaben extrahiert wurde.  In der letzten Spalte ist
angegeben, wann die Aufgabe gestellt wurde, wenn sie schon gestellt wurde,
wobei hier nur Aufgaben aus Olympiaden gelistet werden, die schon
veröffentlicht sind.  Aus technischen Gründen sind eine Reihe von Aufgaben die
parallel in Klasse 9 und 10 gestellt wurden, unter "Status" nur einmal
gelistet. </p> </div>
';

echo showPage($content.AufgabenVorschlaege());
