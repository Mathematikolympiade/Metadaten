<?php
/**
 * User: Hans-Gert Gräbe
 * Date: 2018-12-12
 */

include_once("layout.php");

$content='      
<div class="container">
<div class="row">
<div  class="col-lg-3 col-sm-1"></div><div  class="col-lg-6 col-sm-10">

<p>Hier wird demonstriert, welche Art von Webseiten sich aus den RDF-Quellen
mit kleinen PHP-Skripten erstellen lassen.  Die Beispiele nutzen das <a
href="http://getbootstrap.com" >Bootstrap Framework</a>.  Der Code ist im
git-Repo <a href="https://github.com/Mathematikolympiade/Metadaten"
>https://github.com/Mathematikolympiade/Metadaten</a> verfügbar. </p> 
</div>

<div class="col-lg-3 col-sm-1"> </div> 
</div>

';
echo showPage($content);

?>
