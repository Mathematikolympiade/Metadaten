<?php

require_once "lib/EasyRdf.php";
require_once "thema.php";

use EasyRdf\Graph, EasyRdf\RdfNamespace;

RdfNamespace::set('rdf', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#');
RdfNamespace::set('rdfs', 'http://www.w3.org/2000/01/rdf-schema#');
RdfNamespace::set('math', 'https://www.mathematik-olympiaden.de/aufgaben/rdf/models/math#');
RdfNamespace::set('mo', 'https://www.mathematik-olympiaden.de/aufgaben/rdf/models/mo#');

$graph = new Graph();
$graph->parseFile('../../mdRDF/models/math', 'text/turtle');
$graph->parseFile('../../mdRDF/models/mo', 'text/turtle');
$graph->parseFile('../../mdRDF/buchThemen.ttl', 'text/turtle');

echo $graph->countTriples() . " Triples successfully imported";
//echo $graph->dump();

$resArray = $graph->allOfType("math:Thema");
writeDL($resArray, RdfNamespace::expand("math:Gebiet"));
