@echo off
setlocal enabledelayedexpansion

set out_dir=%1
set branch=%2

set tables= dearborn taylor trenton wayne farmington grosse royal troy;

for %%t in (%tables%) do (
  echo WRITING TABLE %%t
  dolt table import -u rates %out_dir%\%%t.csv --continue
  dolt add .
  dolt commit -m "%%t"
)


dolt push origin %2 --force