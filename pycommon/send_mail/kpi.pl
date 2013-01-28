#!/usr/local/bin/perl

use strict;

use FindBin qw($Bin);
use lib "$Bin/module";
use MyDBI;

if (scalar(@ARGV) < 1)
{
	print STDERR  "./dump2db.pl date\n";
	exit;
}


my $i = $ARGV[0];


my $DATE = `date -d "$i day ago" +%Y%m%d`;

my $j = $i+1;
my $DATEPRE =  `date -d "$j day ago" +%Y%m%d`;

my $VENDOR_ID ="";

my %h_ch = ();
my %h_ch_pre = ();
my %rate = ();
my $pv_tag;
my $active_tag;
my @cloud_vendor = ("cnzz", "pw");


my $dbo = new MyDBI("loganalysis", "loganalysis", "loganalysis");
my $track_id = 0;

foreach my $VENDOR (@cloud_vendor)
{
	if ( $VENDOR eq "pw" )
	{
   		$VENDOR_ID = 100501;
	}

	elsif ( $VENDOR eq "cnzz" )
	{
   		$VENDOR_ID = 100500; 
	}

	$track_id = $dbo->fetch_track_id($VENDOR_ID, "kpi", "cloudsearch_view_click");
	if (0 == $track_id)
	{
		print STDERR "track_id not found: $VENDOR_ID/kpi/cloudsearch_view_click\n";
		next;
	}
	elsif (0 > $track_id)
	{
		print STDERR "More than 1 track_id returned, there should be an bug in:$VENDOR_ID/kpi/cloudsearch_view_click\n";
		next;
	}
	else
	{
		my @result = $dbo->fetch_kpi($track_id, $DATE);
		$h_ch{"pv"} = @result[0];
		$h_ch{"active"} = @result[1];
        $h_ch{"ratio"} = sprintf("%.4f", @result[2]);

		my @result = $dbo->fetch_kpi($track_id, $DATEPRE);
		$h_ch_pre{"pv"} = @result[0];
		$h_ch_pre{"active"} = @result[1];
        $h_ch_pre{"ratio"} = sprintf("%.4f", @result[2]);

		
		$rate{"pv"} = sprintf("%.3f",$h_ch{"pv"} / $h_ch_pre{"pv"} -1) * 100;
		$rate{"active"} = sprintf("%.3f",$h_ch{"active"} / $h_ch_pre{"active"} -1) * 100;
		if ($rate{"pv"} > 0)
		{
			$pv_tag = "&nbsp;<font color='red'>&uarr;</font>";
		}
		else
		{
			$pv_tag = "&nbsp;<font color='green'>&darr;</font>";
		}

		if ($rate{"active"} > 0)
		{
			$active_tag = "&nbsp;<font color='red'>&uarr;</font>";;
		}
		else
		{
		    $active_tag = "&nbsp;<font color='green'>&darr;</font>";
		}

		$rate{"pv"} =abs($rate{"pv"})."%";
		$rate{"active"} =abs($rate{"active"})."%";


		if ($VENDOR eq 'cnzz')
		{
			print "<td>$VENDOR</td><td><font color='red'>$h_ch{'pv'}</font>$pv_tag  $rate{'pv'} </td><td>$h_ch{'active'} </td><td><font color='red'>$h_ch{'ratio'}</font></td>\n\n";
		}
		else
		{
			print "<td>$VENDOR</td><td>$h_ch{'pv'}  $pv_tag $rate{'pv'}</td><td>$h_ch{'active'} </td><td>$h_ch{'ratio'}</td>\n\n";
		}
    	print "</tr>\n";
	}
}	
 

print "</table>\n";
print "<font size=2>KPI计算方式<a href='http://baike.corp.taobao.com/index.php/Cloud_search_log_kpi'>WIKI</a></font>\n";
print "<br></br>\n";


