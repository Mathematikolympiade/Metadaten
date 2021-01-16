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
\@prefix mop: <https://www.mathematik-olympiaden.de/aufgaben/rdf/Aufgabe/> .
\@prefix : <https://www.mathematik-olympiaden.de/aufgaben/rdf/AufgabenVorschlag/> .
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
  my ($g,$s,$m);
  s/\\//gs;
  $g=$1 if /Gebiet\s*\&\s*(.*?)\s*\n/;
  $s=$1 if /Schwierigkeit\s*\&\s*(.*?)\s*\n/;
  $m=$1 if /Status\s*\&\s*(.*?)\s*\n/;
  my @l;
  map { 
    push(@l,"mo:zumGebiet \"$_\""); 
  } split(/\s*,\s*/,$g); 
  map { ;
    # push(@l,"owl:sameAs mop:MO-$_"); 
  } split(/\s*,\s*/,$m); 
  push(@l,"mo:hatSchwierigkeit \"$s\"") if $s;
  my $out=join(" ;\n",@l);
  return <<EOT;
:MO-$nr a mo:AufgabenVorschlag ;
$out .
EOT
}
