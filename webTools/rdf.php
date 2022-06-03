<?php

use EasyRdf\Graph;

require_once "lib/EasyRdf.php";

$graph = new Graph();
$graph->parseFile('../../mdRDF/moGebiete.ttl', 'text/turtle');
//$graph->parseFile('../web/rdf/MO-Basisdaten.rdf');

echo $graph->dump();


