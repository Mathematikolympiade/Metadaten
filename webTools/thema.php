<?php

use EasyRdf\RdfNamespace, EasyRdf\Graph, EasyRdf\Resource;

RdfNamespace::set('rdf', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#');
RdfNamespace::set('rdfs', 'http://www.w3.org/2000/01/rdf-schema#');
RdfNamespace::set('math', 'https://www.mathematik-olympiaden.de/aufgaben/rdf/models/math#');
RdfNamespace::set('mo', 'https://www.mathematik-olympiaden.de/aufgaben/rdf/models/mo#');

class ThemenHandler
{
    public $graph, $themen;
    private $dataBaseDir;
    public $nodeCoreData;

    function __construct($dataBaseDir)
    {
        $this->dataBaseDir = $dataBaseDir;
        $this->graph = new Graph();
        $this->graph->parseFile($this->dataBaseDir . 'models/math', 'text/turtle');
        $this->graph->parseFile($this->dataBaseDir . 'models/mo', 'text/turtle');
        $this->updateThemen();
        $this->nodeCoreData = array();
    }

    private function updateThemen()
    {
        $this->themen = $this->graph->allOfType("math:Thema");
    }

    public function readTTL($fileName)
    {
        $this->graph->parseFile($this->dataBaseDir . $fileName, 'text/turtle');
        $this->updateThemen();
    }

    public function writeDL($thema, $level)
    {
        $themen = array();
        foreach ($this->themen as $thm) if ($thm->get("rdfs:subClassOf") == RdfNamespace::expand($thema)) {
            $themen[] = $thm;
        }
        if (count($themen) > 0) {
            echo '<dl class="mds subject-level-' . $level . '">';
            foreach ($themen as $thm) {
                echo '<dt class="mds subject-level-' . $level . '">' . $thm->label()->getValue() . '</dt>';
                echo '<dd class="mds subject-level-' . $level . '">';
                $this->writeDL($thm->getUri(), $level + 1);
                echo '</dd>';
            }
            echo '</dl>';
        }
    }

    public function writeJsTreeNode($thema, int $level)
    {
        if (is_string($thema)) {
            $rdfNode = RdfNamespace::expand($thema);
        } else {
            $rdfNode = $thema;
//            error_log('else'.$level,3,'error.log');
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
                $this->nodeCoreData[] = array('id' => $thm->localName(),
                    'parent' => $thmParent, 'text' => htmlentities($thm->label()->getValue()));
                $this->writeJsTreeNode($thm, $level + 1);
            }
        }
    }

}

