<?php

require_once "lib/EasyRdf.php";
require_once "themen.php";

$rootThema = $_GET['thema'];
$writer = new ThemenHandler("../../mdRDF/");
$writer->readTTL("buchThemen.ttl");
$writer->writeJsTreeData($rootThema, 0);
error_log(count($writer->jsTreeData),3, 'error.log');
echo json_encode($writer->jsTreeData);
