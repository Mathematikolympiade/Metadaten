<?php
/**
 * User: Hans-Gert Gräbe
 * last update: 2018-04-13
 */

function pageHeader() {
  return '
<!DOCTYPE html>
<html lang="de">
  <head>
    <meta charset="utf-8"/>
    <meta http-equiv="X-UA-Compatible" content="IE=edge"/>
    <meta name="viewport" content="width=device-width, initial-scale=1"/>
    <meta name="description" content="Leipzig Data Demonstration Site"/>
    <meta name="author" content="Leipzig Data Project"/>

    <title>MO Demonstration Site</title>
    <!-- Bootstrap core CSS -->
    <link href="css/bootstrap.min.css" rel="stylesheet"/>
    
  </head>
<!-- end header -->
  <body>

';
}

function pageNavbar() {
  return '

    <!-- Fixed navbar -->
    <nav class="navbar navbar-default" role="navigation">
      <div class="container">        
        <button class="navbar-toggle hidden-sm-up pull-right" type="button"
                data-toggle="collapse" data-target="#navbar"> ☰
        </button>
        <div id="navbar" class="collapse navbar-collapse">  
          <ul class="nav navbar-nav">
            <li><a href="index.php">Startseite</a></li> 
            <li><a href="aufgabenvorschlaege.php">Aufgabenvorschläge</a></li>
            <li><a href="aufgaben.php">Aufgaben</a></li>
            <li><a href="aufgabentexte.php">Aufgabentexte</a></li> 
          </ul>
        </div><!-- collapse end -->
      </div><!-- container end -->
    </nav>';
}

function generalContent() {
  return '
<div class="container">
  <h1 align="center">Demonstations-Site des MO-Projekts</h1>
</div>
';
}

function pageFooter() {
  return '

      <div class="container">
    <div class="footer">
        <p class="text-muted">&copy; MO-Projekt seit 2018 </p>
      </div>
    </div>
    <!-- jQuery (necessary for Bootstrap JavaScript plugins) -->
    <script src="js/jquery.js"></script>
    <!-- Bootstrap core JavaScript -->
    <script src="js/bootstrap.min.js"></script>
    
  </body>
</html>';
}

function showPage($content) {
  return pageHeader().generalContent().pageNavbar().($content).pageFooter();
}
