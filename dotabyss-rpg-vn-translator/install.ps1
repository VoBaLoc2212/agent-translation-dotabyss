param(
    [string]$HermesHome
)

$ErrorActionPreference = "Stop"

if (-not $HermesHome) {
    if ($env:HERMES_HOME) {
        $HermesHome = $env:HERMES_HOME
    }
    else {
        $HermesHome = Join-Path $HOME ".hermes"
    }
}

$Source = Split-Path -Parent $MyInvocation.MyCommand.Path
$Destination = Join-Path $HermesHome "skills\gaming\dotabyss-rpg-vn-translator"

Write-Host "Hermes Home : $HermesHome"
Write-Host "Source      : $Source"
Write-Host "Destination : $Destination"

if (-not (Test-Path (Join-Path $Source "SKILL.md"))) {
    throw "Không tìm thấy SKILL.md trong thư mục cài đặt."
}

New-Item -ItemType Directory -Force -Path $Destination | Out-Null

# Không copy file installer vào skill runtime.
Get-ChildItem -Path $Source -Force |
    Where-Object { $_.Name -ne "install.ps1" } |
    ForEach-Object {
        Copy-Item -Path $_.FullName -Destination $Destination -Recurse -Force
    }

Write-Host ""
Write-Host "Đã cài skill thành công."
Write-Host "Hãy đóng phiên Hermes hiện tại và mở phiên mới."
Write-Host "Kiểm tra bằng: hermes skills list"
Write-Host "Chạy thử bằng: hermes chat -q `"/dotabyss-rpg-vn-translator Hãy mô tả quy trình dịch.`""
