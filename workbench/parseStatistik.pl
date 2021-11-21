use XML::DOM;
use strict;
my $parser=new XML::DOM::Parser;

# Parsen der Statistik-Dateien. Das sollte noch auf den RDF-Cube umgestellt
# werden, um die Information über die Quellen mit darzustellen.
my $out;
map $out.=scan($_), @ARGV;
print TurtleEnvelope($out);

## end main

sub TurtleEnvelope {
  my $out=shift;
  return <<EOT;
\@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
\@prefix ksn: <http://kosemnet.de/Data/Model#> .
\@prefix : <http://kosemnet.de/Data/Aufgabe/> .
\@prefix owl: <http://www.w3.org/2002/07/owl#> .

$out

EOT
}

sub scan { # Verarbeitung der Statistik-Dateien
  my $out;
  my $doc=$parser->parsefile(shift) or die;
  map {
    my $nr=$_->getAttribute("nr");
    my $prozent=$_->getAttribute("prozent");
    $out.=<<EOT if $prozent and $nr=~/\d\d(09|10)\d\d/;
<http://kosemnet.de/Data/Aufgabe/MO-$nr> a ksn:Problem; 
  rdfs:label "MO-Aufgabe $nr"; 
  ksn:hatErfolgsQuote "$prozent" .
EOT
  } $doc->getElementsByTagName("Aufgabe");
  return $out;
}
