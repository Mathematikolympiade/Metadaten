<?php

use EasyRdf\Graph;

require_once "lib/EasyRdf.php";

$graph = new Graph();
$graph->parseFile('../../mdRDF/models/math', 'text/turtle');
$graph->parseFile('../../mdRDF/models/mo', 'text/turtle');
$graph->parseFile('../../mdRDF/moGebiete.ttl', 'text/turtle');

echo $graph->dump();
