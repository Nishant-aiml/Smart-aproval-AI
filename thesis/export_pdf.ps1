param(
    [string]$DocPath = "C:\Users\datta.000\Desktop\shocked\thesis\Smart_Approval_AI_Final_Thesis.docx",
    [string]$PdfPath = "C:\Users\datta.000\Desktop\shocked\thesis\Smart_Approval_AI_Final_Thesis.pdf"
)
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
try {
    $doc = $word.Documents.Open($DocPath, $false, $true, $false)
    $doc.SaveAs([ref]$PdfPath, [ref]17) # 17 = wdFormatPDF
    $doc.Close([ref]$false)
    Write-Output "Successfully exported $DocPath to $PdfPath"
} finally {
    $word.Quit()
}
