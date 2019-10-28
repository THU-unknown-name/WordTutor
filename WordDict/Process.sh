#!/usr/bin/env sh

cat utf-8.txt|sed -e "s/^ *[^ ]\+ \+\([^ ]\+\) .\+/\1/">wordlist.txt

