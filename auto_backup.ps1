Set-Location "C:\Users\Slayer\Documents\masaüstü güç kaynağı"

$changes = git status --porcelain

if ($changes) {
    git add .
    $date = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    git commit -m "Automatic backup - $date"
    git push
}