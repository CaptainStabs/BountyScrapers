@echo off
setlocal enabledelayedexpansion

set out_dir=%1
set com_mess=%2
set branch=%3

dolt checkout main
dolt checkout -b %3

set tables=file insurer code price_metadata rate npi_rate


for /L %%i in (1, 1, 10) do (
  for %%t in (%tables%) do (
    echo WRITING TABLE %%t
    dolt table import -u %%t %out_dir%/%%i/%%t.csv
  )
  dolt gc --shallow
)

dolt add .
dolt commit -m "%2"
dolt push origin %3

python make_pr_cli.py %2 %3