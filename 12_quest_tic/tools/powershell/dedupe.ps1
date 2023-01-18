$uniqueLines = @{}

$lineCount = 61996706
$currentLine = 0

Write-Output "Start"

# Read the file line by line
Get-Content payers.csv -ReadCount 1 | ForEach-Object {
    $currentLine++
    # Add each line to the Hashtable, using the line as the key
    # and a value of $true to indicate that the line has been seen
    $uniqueLines[$_] = $true

    # Calculate the progress as a percentage of the total number of lines
    $progress = [int]($currentLine / $lineCount * 100)

    # Update the progress bar
    Write-Progress -Activity "Deduplicating file" -Status "$currentLine/$lineCount lines processed" -PercentComplete $progress
}

# The Hashtable now contains only unique lines
# You can output the unique lines to a new file using the following command:
$uniqueLines.Keys | Out-File deduped_index.txt
