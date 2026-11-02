$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {
    $docPath = "C:\Users\PC\Downloads\MotionIQ-20261031T053524Z-1-001\MotionIQ\motioniq\MotionIQ_Final_Report_EXE101_EN.docx"
    $pdfPath = "C:\Users\PC\Downloads\MotionIQ-20261031T053524Z-1-001\MotionIQ\motioniq\MotionIQ_Final_Report_EXE101_EN.pdf"
    $doc = $word.Documents.Open($docPath)
    Write-Host ("Page count: " + $doc.ComputeStatistics(2)) # 2 = wdStatisticPages
    $doc.SaveAs([ref]$pdfPath, [ref]17) # 17 = wdFormatPDF
    $doc.Close([ref]0)
    Write-Host "PDF exported successfully!"
} catch {
    Write-Host ("Error: " + $_.Exception.Message)
} finally {
    $word.Quit()
}

