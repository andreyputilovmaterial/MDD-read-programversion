# MDD-read-programversion

This python script helps you programmatically extract program version value from MDD.

The script takes one positional argument, path to MDD,<br />
and prints program version value to stdout.<br />
You can then capture the value in a variable in a BAT file.

For example, type<br />
`python mdmtoolsap-mdd-ver.py p2401215.mdd`<br />
and the script prints "`34`"

See example.bat for possible usage.

This script copies MDD for LI, and makes program version part of folder name.
