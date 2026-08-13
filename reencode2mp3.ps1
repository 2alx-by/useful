$ffmpeg = "C:\tools\ffmpeg\ffmpeg.exe"

Get-ChildItem -Path . -Filter *.flac -File -Recurse | ForEach-Object {
    $flac = $_.FullName
    $mp3  = [System.IO.Path]::ChangeExtension($flac, ".mp3")

    Write-Host "Converting: $flac"

    & $ffmpeg -hide_banner -loglevel error `
        -i $flac `
        -map_metadata 0 `
        -id3v2_version 3 `
        -c:a libmp3lame `
        -q:a 0 `
        -map 0:a:0 `
        $mp3

    # if ($LASTEXITCODE -eq 0 -and (Test-Path $mp3)) {
    if ((Test-Path -LiteralPath $mp3) -and ((Get-Item -LiteralPath $mp3).Length -gt 1024)) {
        Write-Host "  OK -> $mp3" -ForegroundColor Green
        Remove-Item -LiteralPath $flac -Force
    }
    else {
        Write-Host "  FAILED - MP3 missing or <= 1 KB: $mp3" -ForegroundColor Red

        if (Test-Path -LiteralPath $mp3) {
            Write-Host "  MP3 size: $((Get-Item -LiteralPath $mp3).Length) bytes"
            Remove-Item -LiteralPath $mp3 -Force
        }
    }
}
