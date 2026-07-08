<#
terraform apply 이후 API Gateway URL을 frontend/public/config.json에 반영하고 S3에 업로드한다.
사용법: scripts\update-config.ps1
#>

param(
    [string]$TerraformDir = (Join-Path $PSScriptRoot "..\terraform"),
    [string]$ConfigPath = (Join-Path $PSScriptRoot "..\frontend\public\config.json")
)

$ErrorActionPreference = "Stop"

Write-Host "Terraform output에서 API Gateway URL / S3 버킷 이름 조회 중..."
Push-Location $TerraformDir
try {
    $apiUrl = terraform output -raw api_gateway_url
    if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($apiUrl)) {
        throw "terraform output api_gateway_url 조회 실패 (terraform apply가 선행되었는지 확인하세요)"
    }

    $bucketName = terraform output -raw s3_bucket_name
    if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($bucketName)) {
        throw "terraform output s3_bucket_name 조회 실패"
    }
}
finally {
    Pop-Location
}

Write-Host "API Gateway URL: $apiUrl"
Write-Host "S3 버킷: $bucketName"

$config = [ordered]@{ REACT_APP_API_URL = $apiUrl }
$config | ConvertTo-Json | Set-Content -Path $ConfigPath -Encoding utf8
Write-Host "config.json 업데이트 완료: $ConfigPath"

Write-Host "S3에 업로드 중..."
aws s3 cp $ConfigPath "s3://$bucketName/config.json" --content-type "application/json" --cache-control "no-cache"
if ($LASTEXITCODE -ne 0) {
    throw "S3 업로드 실패"
}

Write-Host "완료"
