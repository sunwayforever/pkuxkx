#!/usr/bin/perl
use Encode;
use DBI;

open (INPUT,"<$ARGV[0]") or die "can't open $ARGV[0]";

my $dbh = DBI->connect("dbi:SQLite:dbname=$ARGV[1]","","");

$dbh->do ("drop table npc");
$dbh->do("create table npc (
          _id integer primary key,
          area text,
          room text,
          npc  text)");

my $sth = $dbh->prepare(q{INSERT INTO npc VALUES (null,?,?,?)});

while (<INPUT>) {
    if (/、(.*) /) {
	$current_area = $1;
	next;
    }
    if (/^(\S+)$/) {
	$current_room = $1;
	next;
    }

    if (/^  (.+)$/) {
	$current_npc = $1;
	print "$current_area:$current_room:$current_npc\n";
	$sth->bind_param(1,$current_area);
	$sth->bind_param(2,$current_room);
	$sth->bind_param(3,$current_npc);
	$sth->execute or die $dbh->errstr;
    }
}

$dbh->disconnect;
