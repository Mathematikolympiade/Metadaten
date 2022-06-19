<?php

require_once "lib/EasyRdf.php";

use EasyRdf\RdfNamespace, EasyRdf\Graph;

RdfNamespace::set('rdf', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#');
RdfNamespace::set('rdfs', 'http://www.w3.org/2000/01/rdf-schema#');
RdfNamespace::set('math', 'https://www.mathematik-olympiaden.de/aufgaben/rdf/models/math#');
RdfNamespace::set('mo', 'https://www.mathematik-olympiaden.de/aufgaben/rdf/models/mo#');

class ThemenHandler
{
    public Graph $graph;
    public array $themen;
    private string $dataBaseDir;
    public array $jsTreeData;

    function __construct($dataBaseDir)
    {
        $this->dataBaseDir = $dataBaseDir;
        $this->graph = new Graph();
        $this->graph->parseFile($this->dataBaseDir . 'models/math', 'text/turtle');
        $this->graph->parseFile($this->dataBaseDir . 'models/mo', 'text/turtle');
        $this->updateThemen();
        $this->jsTreeData = array();
    }

    private function updateThemen(): void
    {
        $this->themen = $this->graph->allOfType("math:Thema");
    }

    public function readTTL($fileName): void
    {
        $this->graph->parseFile($this->dataBaseDir . $fileName, 'text/turtle');
        $this->updateThemen();
    }

    public function writeJsTreeData($label, $thema, int $level): void
    {
        if ($level==0) {
            $this->jsTreeData[$label] = array();
        }
        if (is_string($thema)) {
            $rdfNode = RdfNamespace::expand($thema);
        } else {
            $rdfNode = $thema;
        }
        $themen = array();
        foreach ($this->themen as $thm) if ($thm->get("rdfs:subClassOf") == $rdfNode) {
            $themen[] = $thm;
        }
        if (count($themen) > 0) {
            $thmParent = '#';
            if ($level > 0) {
                $thmParent = $rdfNode->localName();
            }
            foreach ($themen as $thm) {
                $this->jsTreeData[$label][] = array('id' => $thm->localName(),
                    'parent' => $thmParent, 'text' => htmlentities($thm->label()->getValue()));
                $this->writeJsTreeData($label, $thm, $level + 1);
            }
        }
    }

}

