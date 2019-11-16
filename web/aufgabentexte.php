<?php
/**
 * User: Hans-Gert Gräbe
 * Date: 2019-11-16 
 * Last Update: 2019-11-16
 *
 */

require_once('lib/EasyRdf.php');
require_once('layout.php');
require_once('helper.php');

function AufgabenTexte() {
  EasyRdf_Namespace::set('mo', 'https://www.mathematik-olympiaden.de/aufgaben/rdf/Model#');
  $graph = new EasyRdf_Graph("http://example.org/Graph/");
  $graph->parseFile("rdf/MO-AufgabenTexte.rdf");
  $res=$graph->resourcesMatching('mo:hatAufgabentext');
  $a=array();
  foreach ($res as $v) {
      $id=str_replace('https://www.mathematik-olympiaden.de/aufgaben/rdf/Aufgabe/','',$v->getURI());
      $text=mehrzeilig($v->get('mo:hatAufgabentext'));
      $a[]='<div class="row"><h4> Aufgabe '.$id.'</h4> <p>'.$text.'</p></div>';
    }
    return '<div class="container">'.join("\n",$a).'</div>';
}

$content='
<div class="container">
<h2 align="center"> Extrahierte Aufgabentexte </h2>

<p>Diese Aufgabentexte wurden von Manuela mit einem Werkzeug aus den
PDF-Vorlagen extrahiert.  Problematisch ist vor allem die Extraktion von
Formeln.</p> </div>
';

echo showPage($content.AufgabenTexte());
