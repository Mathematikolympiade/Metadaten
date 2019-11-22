<?php
/**
 * User: Hans-Gert Gräbe
 * Date: 2019-11-22
 * Last Update: 2019-11-22
 *
 */

require_once('lib/EasyRdf.php');
require_once('layout.php');

function Trans() {
  EasyRdf_Namespace::set('mo', 'https://www.mathematik-olympiaden.de/aufgaben/rdf/Model#');
  $graph = new EasyRdf_Graph("http://example.org/Graph/");
  $graph->parseFile("rdf/moProbleme.rdf");
  $res=$graph->allOfType('mo:Problem');
  $a=array();
  foreach ($res as $v) {
      $nr=$v->get('mo:nr');
      $url=$v->get('mo:pdfA');
      $a[]=':MO-'.$nr.'  a mo:Problem ;
	mo:nr		"'.$nr.'" ;
	mo:pdfA	<'.$url.'> .
';
  }
  return join("\n",$a);
}

echo Trans();
