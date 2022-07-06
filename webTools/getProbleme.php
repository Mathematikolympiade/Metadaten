<?php

require_once "php/procer.php";

header("Access-Control-Allow-Origin: *");

$procer = new ProblemeProcer("../../mdRDF/");
$procer->readTTL("buchThemen.ttl");
$procer->readTTL("buchProbleme.ttl");
$graph = $procer->graph;
//echo $graph->countTriples();

//foreach (json_decode($_GET["themen"]) as $themaID) {
//foreach (["buch_G_01-2", "buch_M_01"] as $themaID) {
foreach (["buch_G_01-2"] as $themaID) {
    $procer->themen[] = $graph->resource("math:" . $themaID);
}
//echo sizeof($procer->themen);
$problemLists = [];
foreach ($procer->themen as $thema) {
    $problemLists[] = $graph->resourcesMatching("math:thm", $thema);
}
$actProblemList = call_user_func_array("array_intersect", $problemLists);
foreach ($actProblemList as $problem) {
    $dataTableEntry = ['id' => $problem->localName()];
    $themenList = array();
    foreach ($problem->allResources("math:thm") as $thm) {
        $themenList[] = htmlentities($thm->label());
    }
    $dataTableEntry['thm'] = $themenList;
    $kurList = array();
    foreach ($problem->allLiterals("math:kur") as $kur) {
        $kurList[] = htmlentities($kur->getValue());
    }
    $dataTableEntry['kur'] = $kurList;
    $procer->dataTableData[] = $dataTableEntry;
}

echo json_encode($procer->dataTableData);
