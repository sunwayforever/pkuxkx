#!/usr/bin/perl
use DBI;

my $dbh = DBI->connect("dbi:SQLite:dbname=/home/sunway/.tt/archive/pkuxkx.db","","");

$dbh->do("create table room (
          _id integer primary key,
          area text,
          room text,
          description  text unique)");

my $sth = $dbh->prepare(q{insert or replace into room VALUES (null,?,?,?)});

while (<>) {
    if (/(.*)@@(.*)@@(.*)/) {
	$area = $1;
	$room = $2;
	$description = $3;

	$sth->bind_param(1,$area);
	$sth->bind_param(2,$room);
	$sth->bind_param(3,$description);
	$sth->execute or die $dbh->errstr;
    }
}

$dbh->disconnect;
