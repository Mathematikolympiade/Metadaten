use strict;

my $out;
map $out.=getKopf($_), @ARGV;
#map $out.=fixValue($_), @ARGV;
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

sub getKopf { # Verarbeitung der Aufgabendateien selbst
  open(FH,shift) or die;
  local $/;
  local $_=<FH>;
  /\\begin\{key\}\s*(\S*)\s*\\end\{key\}/s;
  my $nr=$1;
  $nr=~s|\d+/||;
  /\\begin\{kopf\}(.*)\\end\{kopf\}/s;
  $_=$1;
  my ($g,$s, $o);
  s/\\//gs;
  $g=$1 if /Gebiet\s*\&\s*(.*?)\s*\n/;
  $s=$1 if /Schwierigkeit\s*\&\s*(.*?)\s*\n/;
  $o=$1 if /Status\s*\&\s*(.*?)\s*\n/;
  my @l;
  map { 
    push(@l,"ksn:zumGebiet \"$_\""); 
  } split(/\s*,\s*/,$g); 
  push(@l,"ksn:hatSchwierigkeit \"$s\"") if $s;
  map { 
    push(@l,"owl:sameAs :MO-$_"); 
  } split(/\s*,\s*/,$o); 
  my $out=join(" ;\n",@l);
  return <<EOT;
<http://kosemnet.de/Data/Aufgabe/MO-$nr>
    a ksn:AufgabenVorschlag ;
$out .
EOT
}

sub fixValue {
  open(FH,shift) or die;
  local $/;
  local $_=<FH>;
  /\\begin\{key\}\s*(\S*)\s*\\end\{key\}/s;
  my $nr=$1;
  return <<EOT;
<http://kosemnet.de/Data/Aufgabe/MO-$nr>
    a ksn:AufgabenVorschlag  .
EOT
 
}
