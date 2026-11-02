$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {
    $docPath = "C:\Users\PC\Downloads\MotionIQ-20261031T053524Z-1-001\MotionIQ\motioniq\MotionIQ_Final_Report_EXE101_EN.docx"
    $doc = $word.Documents.Open($docPath)
    
    Write-Host "=== TOTAL PAGES ==="
    $totalPages = $doc.ComputeStatistics(2)
    Write-Host ("Total pages: " + $totalPages)

    Write-Host "`n=== HEADINGS AND THEIR ACTUAL PAGE NUMBERS ==="
    foreach ($p in $doc.Paragraphs) {
        $styleName = $p.Style.NameLocal
        if ($styleName -like "Heading 1*" -or $styleName -like "Heading 2*") {
            $pageNo = $p.Range.Information(3) # 3 = wdActiveEndPageNumber
            $txt = $p.Range.Text.Trim()
            Write-Host ("Page " + $pageNo + " [" + $styleName + "]: " + $txt)
        }
    }

    Write-Host "`n=== TABLES AND THEIR ACTUAL PAGE NUMBERS ==="
    $tIdx = 1
    foreach ($t in $doc.Tables) {
        $pageNo = $t.Range.Information(3)
        $firstCell = $t.Cell(1, 1).Range.Text.Trim()
        Write-Host ("Table " + $tIdx + " on Page " + $pageNo + " (First cell: " + $firstCell + ")")
        $tIdx++
    }

    $doc.Close([ref]0)
} catch {
    Write-Host ("Error: " + $_.Exception.Message)
} finally {
    $word.Quit()
}

