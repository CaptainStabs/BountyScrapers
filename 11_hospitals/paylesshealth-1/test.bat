@echo off
for %%x in (.\\submitted\\*) do (
  dolt table import -u hospitals %%x --continue
)
