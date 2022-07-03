<?php

require_once "php/procer.php";

header("Access-Control-Allow-Origin: *");

$procer = new ThemenProcer("../../mdRDF/");
$procer->readTTL("buchThemen.ttl");
$procer->writeJsTreeData("gebiete", "math:Gebiet", 0);
$procer->writeJsTreeData("methoden", "math:Methode", 0);
echo json_encode($procer->jsTreeData);
