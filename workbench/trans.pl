open(FH,"a.n3") or die;
$hash;
while (<FH>) {
  chomp;
  $hash=process($hash,$_);
}

my $out;
map $out.=entry($hash->{$_}), (keys %$hash);
print $out;

sub entry {
  my $u=shift;
  my $id=$u->{"Id"}; 
  my $aufgabe=$u->{"Aufgabe"}; 
  my $oly=$u->{"oly"}; 
  my $okl=$u->{"okl"}; 
  my $rnd=$u->{"rnd"}; 
  return <<EOT ;
:$id a qb:Observation;
  qb:dataSet :theDataset ; 
  mo:Aufgabe mop:$aufgabe;
  mo:okl "$okl" ;
  mo:oly "$oly" ;
  mo:rnd "$rnd" .

EOT
}
	    
	  
sub process {
  my $hash=shift;
  local $_=shift; 
  if (s/^(_:\w+)\s*//) {
    my $id=$1; 
    m|#(\w+)>\s*"(\w+)"|;
    $hash->{$id}{$1}=$2;
    $hash->{$id}{"Id"}=$id;
  }
  if (s/(_:\w+)//) {
    my $id=$1;
    m|(MO-\d+)|;
    $hash->{$id}{"Aufgabe"}=$1;
  }
  return $hash;
}
	   
