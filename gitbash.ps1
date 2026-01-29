# iwr -useb https://raw.githubusercontent.com/Piyush-linux/practical/refs/heads/master/gitbash.ps1 | iex


$ErrorActionPreference = "Stop"

$gitUrl = "https://github.com/git-for-windows/git/releases/download/v2.52.0.windows.1/Git-2.52.0-64-bit.exe"
#$gitUrl="https://cachefly.alfredapp.com/Alfred_5.7.2_2312.dmg"
$out = "Git-Bash-Installer.exe"

Write-Host "Downloading Git Bash installer..."

if (Get-Command curl -ErrorAction SilentlyContinue)
{
    # curl -L -o $out $gitUrl
    Invoke-WebRequest -Uri $gitUrl -OutFile $out
} else
{
    # Fix TLS for Windows 7
    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
    Invoke-WebRequest -Uri $gitUrl -OutFile $out
}

Write-Host "✅ Downloaded to $out"
