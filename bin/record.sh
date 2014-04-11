#!/bin/bash
arg=`echo $1|iconv -f gbk -t utf8 `;
arg=`echo $arg|sed 's/[、。，,. 「」！』『【】;]//g'`;

echo $arg|~/.tt/bin/record.pl &>/dev/null
