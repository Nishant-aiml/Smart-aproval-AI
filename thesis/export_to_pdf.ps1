$docxPath = "C:\Users\datta.000\Desktop\shocked\thesis\Smart_Approval_AI_Final_Thesis.docx"
$pdfPath = "C:\Users\datta.000\Desktop\shocked\thesis\Smart_Approval_AI_Final_Thesis.pdf"

if (Test-Path $pdfPath) {
    Remove-Item $pdfPath -Force
}

$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0

try {
    $doc = $word.Documents.Open($docxPath)
    $pages = $doc.ComputeStatistics(2) # 2 = wdStatisticPages
    Write-Host "Word Computed Page Count: $pages"
    $doc.ExportAsFixedFormat($pdfPath, 17) # 17 = wdExportFormatPDF
    Write-Host "Successfully exported PDF via Word COM."
    $doc.Close([ref]$false)
} catch {
    Write-Error $_
} finally {
    $word.Quit()
}
