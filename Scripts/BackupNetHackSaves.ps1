param([string]$Reason='manual')
$ErrorActionPreference='Stop'
$python=Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
if(!(Test-Path -LiteralPath $python)){$python=(Get-Command python -ErrorAction Stop).Source}
& $python (Join-Path $PSScriptRoot 'NetHackSaveBackup.py') backup --reason $Reason
if($LASTEXITCODE -ne 0){throw 'Save backup failed. Existing saves were not changed.'}
