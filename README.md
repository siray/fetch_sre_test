# fetch_sre_test
## FETCH SRE in Test, Take Home Test

This project is written in python and should be run with "python main.py" command

Input file should be given as path via console by user

All HTTP method types are specified in main.py regardless of their usability to check health of a url (for instance I wouldn't use DELETE to check a health of a url) to support any endpoint in input file

GET Request to https://www.fetchrewards.com/ url gives 301 Moved Permanently either in code or with curl command so its result was always false while testing
