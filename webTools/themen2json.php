<?php

require_once "lib/EasyRdf.php";
require_once "thema.php";


$writer = new ThemenHandler("../../mdRDF/");
$writer->readTTL("buchThemen.ttl", 'text/turtle');
$writer->writeJsTreeNode("math:Gebiet", 0);
$jsTreeData = json_encode($writer->nodeCoreData);
?>

<!DOCTYPE html>
<html lang="de">
<header>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/jstree/3.2.1/themes/default/style.min.css"/>
    <!--    <link rel="stylesheet" type="text/css" href="rdf.css"/>-->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jstree/3.2.1/jstree.min.js"></script>
    <script type="application/javascript">
        $(function () {
            let jsTreeData = <?php echo $jsTreeData; ?>;
            let jsTreeJSON = {"core": {"themes": {"dots": false, "stripes": true}, "data": jsTreeData}};
            $("#treeview").jstree(jsTreeJSON);
        })
    </script>
</header>
<body>
<h2>Thematisches Register</h2>
<div id="treeview"></div>
</body>
</html>
