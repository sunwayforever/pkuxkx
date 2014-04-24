@echo off
set dir=%cd%
cd ..
%dir%/mintty.exe -c %dir%/mintty.con -e %dir%/tt++.exe main.tin