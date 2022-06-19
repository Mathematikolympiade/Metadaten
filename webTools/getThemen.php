<?php

require_once "themen.php";

$writer = new ThemenHandler("../../mdRDF/");
$writer->readTTL("buchThemen.ttl");
$writer->writeJsTreeData("gebiete", "math:Gebiet", 0);
$writer->writeJsTreeData("methoden", "math:Methode", 0);
echo json_encode($writer->jsTreeData);
