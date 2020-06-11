# Globals - Modify these lines to match your environment's paths
$zipPath = "C:\Program Files\7-Zip\7z.exe"
$WorkPath = "D:\zipTest"
$contentsDirectory = "ArchivePDF"
$logFile = "zipLog.txt"
$zipExt = ".zip"

# Input Arguments
if (!($zipExt.StartsWith('.'))) {
    $zipExt = '.' + $zipExt
}

# Globals - For measuring average time of compression algorithm
[System.Collections.ArrayList]$mx3 = @()
[System.Collections.ArrayList]$mx5 = @()
[System.Collections.ArrayList]$mx7 = @()
[System.Collections.ArrayList]$mx9 = @()
[System.Collections.ArrayList]$LZMA = @()

# Check if paths exists and remove old log file
if (!(Test-Path -Path $WorkPath))
    { Throw "Directory $WorkPath does not exist" }
if (!(Test-Path -Path (Join-Path $WorkPath $contentsDirectory)))
    { Throw "Directory $contentsDirectory does not exist" }
if (!(Test-Path -Path $zipPath))
    { Throw "Executable $zipPath does not exist" }
if (Test-Path -Path (Join-Path $WorkPath $logFile))
    { Remove-Item (Join-Path $WorkPath $logFile) }

# Function - Format and display the TimeSpan value.
function writeTime($sw, [string]$zip) {
    $elapsedTime = $sw.Minutes*60 + $sw.Seconds + $sw.Milliseconds/1000
    Write-Output "$zip $elapsedTime seconds" | Out-File -FilePath (Join-Path $WorkPath $logFile) -Append
    switch($zip) {
        "-mx=3" { $mx3.Add($elapsedTime) }
        "-mx=5" { $mx5.Add($elapsedTime) }
        "-mx=7" { $mx7.Add($elapsedTime) }
        "-mx=9" { $mx9.Add($elapsedTime) }
        "-m0=LZMA" { $LZMA.Add($elapsedTime) }
    }
}

# Function - Get average time from list
function getAvg($list) {
    $total = 0
    foreach ($time in $list) {
        $total += $time
    }
    return ($total / $list.Count)
}

# Function - Cleanup zip archives when beginning each iteration of the main loop
function cleanupZips() {
    Set-Location $WorkPath
    Get-ChildItem -Filter *$zipExt -File -Recurse | ForEach-Object {
        Remove-Item $_.FullName -Force -Recurse 
    }
}

# Function - Start a stopwatch and time the zip process using the provided compression level
function runZipProcess($compressionLevel) {
    $sw = [Diagnostics.Stopwatch]::StartNew()
    Start-Process $zipPath -ArgumentList "a -tzip $compressionLevel .\$compressionLevel$zipExt .\$contentsDirectory\*" -wait
    $sw.Stop()
    writeTime $sw.Elapsed $compressionLevel
}

# Main Loop - Goes over 5 iterations by default for a more accurate average.
For ([int]$i = 0; $i -lt 3; $i++) {
    Write-Host "Running zip pass #$($i + 1)"
    cleanupZips -wait
    runZipProcess "-mx=3" | Out-null
    runZipProcess "-mx=5" | Out-null
    runZipProcess "-mx=7" | Out-null
    runZipProcess "-mx=9" | Out-null
    runZipProcess "-m0=LZMA" | Out-null
}

# Get average times and output to log
Write-Output "-mx=3 $(getAvg $mx3) seconds (avg)" | Out-File -FilePath ".\$logFile" -Append
Write-Output "-mx=5 $(getAvg $mx5) seconds (avg)" | Out-File -FilePath ".\$logFile" -Append
Write-Output "-mx=7 $(getAvg $mx7) seconds (avg)" | Out-File -FilePath ".\$logFile" -Append
Write-Output "-mx=9 $(getAvg $mx9) seconds (avg)" | Out-File -FilePath ".\$logFile" -Append
Write-Output "-m0=LZMA $(getAvg $LZMA) seconds (avg)" | Out-File -FilePath ".\$logFile" -Append
Write-Host "Job complete - see $WorkPath\$logFile"
