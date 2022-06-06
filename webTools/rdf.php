<?php

require_once "lib/EasyRdf.php";
require_once "thema.php";



$writer = new ThemenHandler("../../mdRDF/");
$writer->readTTL("buchThemen.ttl", 'text/turtle');

echo $writer->graph->countTriples() . " Triples successfully imported";
?>

<html lang="de">
<header>
    <link rel="stylesheet" type="text/css" href="rdf.css"/>
    <script type="application/javascript">
    </script>
</header>
<body>
<h2>Thematisches Register</h2>
<?php $writer->writeDL("math:Gebiet", 0); ?>
</body>
</html>
