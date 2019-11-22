use strict;

my $out;
map $out.=getKopf($_), @ARGV;
print TurtleEnvelope($out);

## end main

sub TurtleEnvelope {
  my $out=shift;
  return <<EOT;
\@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
\@prefix mo: <https://www.mathematik-olympiaden.de/aufgaben/rdf/Model#> .
\@prefix : <https://www.mathematik-olympiaden.de/aufgaben/rdf/AufgabenVorschlag/> .
\@prefix mop: <https://www.mathematik-olympiaden.de/aufgaben/rdf/Aufgabe/> .
\@prefix owl: <http://www.w3.org/2002/07/owl#> .

$out

EOT
}

sub getKopf { # Verarbeitung der Aufgabendateien selbst
  open(FH,shift) or die;
  local $/;
  local $_=<FH>;
  /\\begin\{key\}\s*(\S*)\s*\\end\{key\}/s;
  my $nr=$1;
  $nr=~s|\d+/||;
  /\\begin\{kopf\}(.*)\\end\{kopf\}/s;
  $_=$1;
  my ($o);
  s/\\//gs;
  $o=$1 if /Status\s*\&\s*(.*?)\s*\n/;
  return unless $o;
  $o=~s/(\d+)/mop:MO-$1/gs;
  return <<EOT ;
:MO-$nr owl:sameAs $o .
EOT
}
