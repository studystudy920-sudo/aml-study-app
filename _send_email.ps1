$config = Get-Content "C:\Users\masak\.claude\email_config.json" | ConvertFrom-Json
if ($config.app_password -eq "XXXX XXXX XXXX XXXX") {
  Write-Output "EMAIL_NOT_CONFIGURED: set app_password in email_config.json"
  exit 0
}
Write-Output "EMAIL_CONFIGURED: would send to $($config.email)"
