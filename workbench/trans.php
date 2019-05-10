<?php

/** Transformiere die Aufgabenextrakte aus Manuelas Dump der Datenbank in
 * RDF. 

 Version: 2019-05-10

 **/

function getConnection() {
    try {
        $dbh = new PDO('mysql:host=localhost;dbname=graebe;charset=utf8', "graebe", ""); 
    } catch (PDOException $e) {
        print "Error!: " . $e->getMessage() . "<br/>";
        die();
    }
    return $dbh;
}

function db_query($query) {
    $dbh = getConnection();
    return $dbh->query($query);
}

function getData() {
    $res=db_query("select * from moev2017_aufgaben");
    $s=array();
    foreach ($res as $row) {
        $nr=$row['number'];
        $text=fixText($row['text']);
        $s[]=':MO-'.$nr.' mo:hatAufgabentext """'.$text.'""" .';
    }
    return join("\n\n",$s);
}

function fixText($s) {
    $s=str_replace('','',$s);
    $s=str_replace('','',$s);
    $s=str_replace('\\','',$s);
    $s=preg_replace('/^\d+/','',$s);

    return trim($s)." ";
}

function TurtlePrefix() {
    return '
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix : <https://www.mathe-wettbewerbe.de/mo/rdf/Aufgabe/> .
@prefix mo: <https://www.mathe-wettbewerbe.de/mo/rdf/Model#> .
@prefix mog: <https://www.mathe-wettbewerbe.de/mo/rdf/Gebiet/> .
';
}

echo TurtlePrefix().getData();