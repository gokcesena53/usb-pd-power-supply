Set-Location $PSScriptRoot

$changes = git status --porcelain

if ($changes) {
    git add .
    $date = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    git commit -m "Automatic backup - $date"
    git push
}