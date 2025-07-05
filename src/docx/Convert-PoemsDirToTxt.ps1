$docxPath = "$HOME\OneDrive\Desktop\poems_backup\docx"
$txtPath = "$HOME\OneDrive\Desktop\poems_backup"

Get-ChildItem -Path $docxPath -File | ForEach-Object {
    $curFull = $_.FullName
    $curExt = $_.Extension
    $curBase = $_.BaseName
    if ($curExt -eq ".docx") {
        $txtFile = "$txtPath\$curBase.txt"
        Write-Host "converting file: $curFull"
        & "$HOME/OneDrive/Documents/PowerShell/Scripts/Convert-DocxToTxt.ps1" -docxPath $curFull -txtPath $txtFile
    }
    else {
        "Skipping file $curBase"
    }
}
