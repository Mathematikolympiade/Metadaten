<?php
/**
 * User: Hans-Gert Gräbe
 * last update: 2021-01-16
 */

function pageHeader() {
  return '
<!DOCTYPE html>
<html lang="de">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">

    <meta name="description" content="MO Metadata Project Demonstration Site"/>
    <meta name="author" content="MO Metadata Project"/>

    <title>MO Metadata Project Demonstration Site</title>
    
  </head>
<!-- end header -->
  <body>

';
}

function pageNavbar() {
  return '

    <!-- Fixed navbar -->
    <nav class="navbar navbar-expand-lg bg-light">
      <div class="container">        
        <button class="navbar-toggler" type="button" data-toggle="collapse"
                data-target="#navbar" aria-controls="navbarNavAltMarkup"
                aria-expanded="false" aria-label="Toggle navigation"> ☰
        </button>
        <div id="navbar" class="collapse navbar-collapse">  
          <ul class="nav navbar-nav mr-auto">
            <li class="nav-link"><a href="index.php">Startseite</a></li> 
            <li class="nav-link"><a href="aufgabenvorschlaege.php">Aufgabenvorschläge</a></li>
            <li class="nav-link"><a href="aufgaben.php">Aufgaben</a></li>
            <li class="nav-link"><a href="gebiete.php">Gebiete</a></li>
            <!-- <li class="nav-link"><a href="aufgabentexte.php">Aufgabentexte</a></li> --> 
          </ul>
        </div><!-- collapse end -->
      </div><!-- container end -->
    </nav>';
}

function generalContent() {
  return '
<div class="container">
  <h1 align="center">Demonstrations-Site des MO Metadaten Projekts</h1>
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

<!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js" integrity="sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbBJiSnjAK/l8WvCWPIPm49" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js" integrity="sha384-ChfqqxuZUCnJSK3+MXmPNIyE6ZbWh2IMqE241rYiqJxyMiZ6OW/JmZQ5stwEULTy" crossorigin="anonymous"></script>
  </body>
</html>';
}

function showPage($content) {
  return pageHeader().generalContent().pageNavbar().($content).pageFooter();
}
