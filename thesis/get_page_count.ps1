param([string]$DocPath = "C:\Users\datta.000\Desktop\shocked\thesis\test_50_pages.docx")
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
try {
    $doc = $word.Documents.Open($DocPath, $false, $true, $false)
    $pages = $doc.ComputeStatistics(2)
    $words = $doc.ComputeStatistics(0)
    Write-Output "PAGE COUNT: $pages pages, $words words in $DocPath"
    $doc.Close([ref]$false)
} finally {
    $word.Quit()
}
