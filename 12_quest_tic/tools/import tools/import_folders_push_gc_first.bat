@echo off
setlocal enabledelayedexpansion

set out_dir=%1
set com_mess=%2
set branch=%3

set tables=plans files plans_files codes provider_groups prices prices_provider_groups

dolt push origin uhc_pt3
dolt gc
for /L %%i in (1, 1, 10) do (
  for %%t in (%tables%) do (
    echo WRITING TABLE %%t
    dolt table import -u %%t %out_dir%/%%i/%%t.csv
  )
)

dolt add .
dolt commit -m "%2"
dolt push origin %3