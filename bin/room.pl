#!/usr/bin/perl
use DBI;

open (INPUT,"<$ARGV[0]") or die "can't open $ARGV[0]";

my $dbh = DBI->connect("dbi:SQLite:dbname=$ARGV[1]","","");

$dbh->do ("drop table room");
$dbh->do("create table room (
          _id integer primary key,
          area text,
          room text,
          description  text)");

my $sth = $dbh->prepare(q{INSERT INTO room VALUES (null,?,?,?)});

while (<INPUT>) {
    next if /^$/;
    if (/(^\S+)$/) {
	$current_area = $1;
	next;
    }
    if (/^(\S+)\s+(.+)$/) {
	$current_room = $1;
	$current_description = $2;
	print "$current_area:$current_room:$current_description\n";

	$sth->bind_param(1,$current_area);
	$sth->bind_param(2,$current_room);
	$sth->bind_param(3,$current_description);
	$sth->execute or die $dbh->errstr;
    }
}

$dbh->disconnect;
