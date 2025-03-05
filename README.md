# MDD-read-programversion

this python script helps you programmatically extract program version value from MDD

the script takes one positional argument, path to MDD
and prints program version value to stdout
you can then capture the value to a variable in a BAT file

from example, type
python mdmtoolsap-mdd-ver.py p2401215.mdd
and the script prints "34"

see example.bat for possible usage

this script copies MDD for LI, and makes program version part of folder name
