#!/usr/bin/perl

$OFF='01080500';
$ON ='01080501';

#これが電球のマックアドレス
#$ADDR='A3:39:71:95:B0:BC';
#$ADDR='27:A3:A2:F9:49:99';

$head='55AA';

$RGB='FFFFFF';

if ($#ARGV<0) {
    print <<EOF;
Usage:
  $0 on       Turn on.
  $0 off      Turn off.
  $0 RRGGBB   Change color.
EOF
    exit;
}

if ($ARGV[0] =~ /^([0-9a-fA-F]{6})$/o) {
    $RGB=$ARGV[0];	
    #print "RGB=",$RGB,"\n";
}
$body='030802'. $RGB;

$body=$ON if $ARGV[0] =~ /^on/o;
$body=$OFF if $ARGV[0] =~ /^off/o;

$ADDR = $ARGV[1];
foreach($body =~ /../g) {
    $sum += hex($_);
}
$sum = sprintf("%02X",((~$sum)+1) & 0xff);

$CMD="/usr/bin/gatttool -b $ADDR --char-write-req --handle=0x000c --value=".$head.$body.$sum;

#print $CMD,"\n";
system($CMD);


    
