@echo off
setlocal enabledelayedexpansion

set out_dir=%1

set tables=plans files plans_files codes provider_groups prices prices_provider_groups

for %%t in (%tables%) do (
  echo WRITING TABLE %%t
  dolt table import -u %%t %out_dir%/%%t.csv
)
