<?php

require_once "libs/EasyRdf.php";

use EasyRdf\RdfNamespace, EasyRdf\Graph;

RdfNamespace::set('rdf', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#');
RdfNamespace::set('rdfs', 'http://www.w3.org/2000/01/rdf-schema#');
RdfNamespace::set('math', 'https://www.mathematik-olympiaden.de/aufgaben/metadaten/models/math#');
RdfNamespace::set('mo', 'https://www.mathematik-olympiaden.de/aufgaben/metadaten/models/mo#');

class TtlProcer
{
    protected string $baseDir;
    public string $modelDir = "models/";
    public array $modelList = ["math", "mo"];
    public Graph $graph;

    function __construct($baseDir)
    {
        $this->baseDir = $baseDir;
        $this->graph = new Graph();
        foreach ($this->modelList as $model) {
            $filename = $this->baseDir . $this->modelDir . $model;
            $this->graph->parseFile($filename, 'text/turtle');
        }
    }
}

class ThemenProcer extends TtlProcer
{
    public array $themen;
    public array $jsTreeData;

    function __construct($baseDir)
    {
        parent::__construct($baseDir);
        $this->updateThemen();
        $this->jsTreeData = array();
    }

    private function updateThemen(): void
    {
        $this->themen = $this->graph->allOfType("math:Thema");
    }

    public function readTTL($fileName): void
    {
        $this->graph->parseFile($this->baseDir . $fileName, 'text/turtle');
        $this->updateThemen();
    }

    public function writeJsTreeData($label, $thema, int $level): void
    {
        if ($level == 0) {
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

class ProblemeProcer extends TtlProcer
{
    public array $themen;
    public array $dataTableData;

    function __construct($baseDir)
    {
        parent::__construct($baseDir);
        $this->dataTableData = [];
    }

    public function readTTL($fileName): void
    {
        $this->graph->parseFile($this->baseDir . $fileName, 'text/turtle');
    }


}
