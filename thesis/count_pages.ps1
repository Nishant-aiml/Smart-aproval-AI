$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
try {
    $doc = $word.Documents.Open("C:\Users\datta.000\Desktop\shocked\thesis\Smart_Approval_AI_Final_Thesis.docx", $false, $true, $false)
    $pages = $doc.ComputeStatistics(2) # 2 = wdStatisticPages
    $words = $doc.ComputeStatistics(0) # 0 = wdStatisticWords
    Write-Output "EXACT WORD PAGE COUNT: $pages pages, $words words"
    $doc.Close([ref]$false)
} finally {
    $word.Quit()
}
