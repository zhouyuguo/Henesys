#!/usr/local/bin/perl

use strict;

use FindBin qw($Bin);
use lib "$Bin/module";
use MyDBI;

if (scalar(@ARGV) < 2)
{
	print "./dump2db.pl vendor date\n";
	exit;
}


my $VENDOR = $ARGV[0];
my $i = $ARGV[1];
open IN, "$ARGV[2]" or die $!;

my $DATE = `date -d "$i day ago" +%Y%m%d`;
my $VENDOR_ID ="";
my @cloud_search_channel =();
my @cloud_recommend_channel =();

if ( $VENDOR eq "pw" )
{
   $VENDOR_ID = 100501; 
   @cloud_search_channel =("ssrp","ss_drag", "search");
   @cloud_recommend_channel =("wprdsp","hkwrdsp","wpr_pop","wpr_refer","recommend");
}
elsif ( $VENDOR eq "cnzz" )
{
   $VENDOR_ID = 100500; 
   @cloud_search_channel =("ssrp","ss_highlight","ss_drag","ss_hwpop","search");
   @cloud_recommend_channel =("wprdsp","hkwrdsp","wpr_pop","wpr_refer","hw_highlight","recommend");
}

my %h_ch = ();
my %channel_name = ();
my @cloud_channel =("ssrp","ss_highlight","ss_drag","ss_hwpop","wprdsp","hkwrdsp","wpr_pop","wpr_refer","hw_highlight");


while(<IN>)
{
	my $line = $_;
	chomp $line;
	my @arr = split '\t', $line;
    $channel_name{$arr[0]} = $arr[1];

}
my $dbo = new MyDBI("loganalysis", "loganalysis", "loganalysis");
my $track_id = 0;

foreach my $ch (@cloud_search_channel)
{
	$track_id = $dbo->fetch_track_id($VENDOR_ID, $ch, "cloudsearch_view_click");
	if (0 == $track_id)
	{
		print STDERR "track_id not found: $VENDOR_ID/$ch/cloudsearch_view_click\n";
		next;
	}
	elsif (0 > $track_id)
	{
		print STDERR "More than 1 track_id returned, there should be an bug in:$VENDOR_ID/$ch/cloudsearch_view_click\n";
		next;
	}
	else
	{
		my @result = $dbo->fetch_pv_click_ratio($track_id, $DATE);
		$h_ch{$ch}{"pv"} = @result[0];
		$h_ch{$ch}{"click"} = @result[1];
        $h_ch{$ch}{"ratio"} = sprintf("%.3f", @result[2]);

		print "<td>$channel_name{$ch}</td><td>$h_ch{$ch}{'pv'}</td><td>$h_ch{$ch}{'click'}</td><td>$h_ch{$ch}{'ratio'}</td>\n\n";
    	print "</tr>\n";
	}
}	
 

print "</table>\n";
print "<br></br>\n";


