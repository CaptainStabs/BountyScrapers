# Get the total number of lines in the input file
$lineCount = 61996706

# Create a Stopwatch object to measure elapsed time
$stopwatch = [System.Diagnostics.Stopwatch]::StartNew()

# Read the input file line by line and select the unique lines
$uniqueLines = Get-Content payers.csv -Encoding UTF8 | Select-Object -Unique