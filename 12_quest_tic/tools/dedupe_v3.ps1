$uniqueLines = @{}

$lineCount = 61996706
$currentLine = 0
$duplicateCount = 0

# Create a Stopwatch object to measure elapsed time
$stopwatch = [System.Diagnostics.Stopwatch]::StartNew()

# Read the file line by line
Get-Content payers.csv -ReadCount 1 -Encoding UTF8 | ForEach-Object {
    $currentLine++ # Increment for progress

    # Add each line to the Hashtable, using the line as the key
    # and a value of $true to indicate that the line has been seen
    if ($uniqueLines.ContainsKey($_)) {
        $duplicateCount++
    } else {
        $uniqueLines[$_] = $true
    }


    # Calculate the progress as a percentage of the total number of lines
    $progress = [int]($currentLine / $lineCount * 100)

    # Prevent dbz errors
    if ($duplicateCount -gt 0) {
        $duplicate_percent = [int]($duplicateCount / $currentLine * 100)
    } else {
        $duplicate_percent = 0
    }

    # Calculate the elapsed time and the estimated time remaining
    $elapsedTime = $stopwatch.Elapsed
    $eta = [System.TimeSpan]::FromTicks($elapsedTime.Ticks / $currentLine * ($lineCount - $currentLine))

    # Format the elapsed time and ETA as strings
    $elapsedTimeString = "{0:D2}h:{1:D2}m:{2:D2}s" -f $elapsedTime.Hours, $elapsedTime.Minutes, $elapsedTime.Seconds
    $etaString = "{0:D2}h:{1:D2}m:{2:D2}s" -f $eta.Hours, $eta.Minutes, $eta.Seconds

    # Update the progress bar
    Write-Progress -Activity "Deduplicating file" -Status "$currentLine/$lineCount lines processed" -PercentComplete $progress -CurrentOperation "$elapsedTimeString elapsed, ETA: $etaString, duplicates found: $duplicateCount, $duplicate_percent% duplicate"
}

# The Hashtable now contains only unique lines
# Output the unique lines to a new file using the following command
Write-Output "Counting unique lines..."
$uniqueLineCount = $uniqueLines.Keys.Count
$currentLine = 0

Write-Output("There are $uniqueLineCount unique lines")

# Loop through the unique lines and write them to the output file (done this way to have progress bar)
$stopwatch2 = [System.Diagnostics.Stopwatch]::StartNew()
foreach ($line in $uniqueLines.Keys) {
    $currentLine++
    # Calculate the progress as a percentage of the total number of unique lines
    $progress = [int]($currentLine / $uniqueLineCount * 100)

    $elapsedTime = $stopwatch2.Elapsed
    $eta = [System.TimeSpan]::FromTicks($elapsedTime.Ticks / $currentLine * ($lineCount - $currentLine))

    # Format the elapsed time and ETA as strings
    $elapsedTimeString = "{0:D2}h:{1:D2}m:{2:D2}s" -f $elapsedTime.Hours, $elapsedTime.Minutes, $elapsedTime.Seconds
    $etaString = "{0:D2}h:{1:D2}m:{2:D2}s" -f $eta.Hours, $eta.Minutes, $eta.Seconds

    # Update the progress bar
    Write-Progress -Activity "Writing Output File" -Status "$currentLine/$uniqueLineCount lines written" -PercentComplete $progress

    # Write the line to the output file
    $line | Out-File test_dedupe.txt -Append
}


# Stop the Stopwatch object
$stopwatch.Stop()

$elapsedTime = $stopwatch.Elapsed
$elapsedTimeString = "{0:D2}h:{1:D2}m:{2:D2}s" -f $elapsedTime.Hours, $elapsedTime.Minutes, $elapsedTime.Seconds

# Print the number of duplicates found
Write-Output "Number of duplicates found: $duplicateCount"
Write-Output "Took $elapsedTimeString"