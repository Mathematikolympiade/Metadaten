<?php

use EasyRdf\RdfNamespace;

function writeDL($resArray, $thema) {
    foreach ($resArray as $res) {
//    echo $res->dump("text") ;
        if ($res->get("rdfs:subClassOf")==$thema) {
            echo "\n<dt>".$res->label()."</dt>";
            echo "\n<dd><dl>";
            writeDL($resArray, $res->getUri());
            echo "\n</dl></dd>";
        }
    }
}
