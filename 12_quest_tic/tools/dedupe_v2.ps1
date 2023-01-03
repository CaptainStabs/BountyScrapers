$uniqueLines = @{}

$lineCount = 61996706
$currentLine = 0
$chunk_size = 1

# Create a Stopwatch object to measure elapsed time
$stopwatch = [System.Diagnostics.Stopwatch]::StartNew()

# Read the file line by line
Get-Content payers.csv -ReadCount $chunk_size | ForEach-Object {
    # $currentLine++
    $currentLine = $currentLine + $chunk_size
    # Add each line to the Hashtable, using the line as the key
    # and a value of $true to indicate that the line has been seen
    $uniqueLines[$_] = $true

    # Calculate the progress as a percentage of the total number of lines
    $progress = [int]($currentLine / $lineCount * 100)

    # Calculate the elapsed time and the estimated time remaining
    $elapsedTime = $stopwatch.Elapsed
    $eta = [System.TimeSpan]::FromTicks($elapsedTime.Ticks / $currentLine * ($lineCount - $currentLine))

    # Format the elapsed time and ETA as strings
    $elapsedTimeString = "{0:D2}h:{1:D2}m:{2:D2}s" -f $elapsedTime.Hours, $elapsedTime.Minutes, $elapsedTime.Seconds
    $etaString = "{0:D2}h:{1:D2}m:{2:D2}s" -f $eta.Hours, $eta.Minutes, $eta.Seconds
    # Update the progress bar
    Write-Progress -Activity "Deduplicating file" -Status "$currentLine/$lineCount lines processed" -PercentComplete $progress -CurrentOperation "$elapsedTimeString elapsed, ETA: $etaString"
}

Write-Output $uniqueLines

# The Hashtable now contains only unique lines
# You can output the unique lines to a new file using the following command:
$uniqueLines.Keys | Out-File deduped_payers.txt

# Stop the Stopwatch object
$stopwatch.Stop()
