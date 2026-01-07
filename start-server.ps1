# Start HTTP Server for Praison Labs website
$port = 8000
$directory = "c:\Downloaded Web Sites\www.praisonlabs.com"

Write-Host "Starting HTTP server on port $port..."
Write-Host "Serving files from: $directory"
Write-Host ""
Write-Host "Website will be available at:"
Write-Host "  http://localhost:$port/index.htm"
Write-Host "  http://localhost:$port/"
Write-Host ""
Write-Host "Press Ctrl+C to stop the server"
Write-Host ""

Set-Location $directory
python -m http.server $port


