$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {
    $docPath = "C:\Users\PC\Downloads\MotionIQ-20261031T053524Z-1-001\MotionIQ\motioniq\MotionIQ_Final_Report_EXE101_EN.docx"
    $doc = $word.Documents.Open($docPath)
    
    Write-Host "=== SECTIONS AND THEIR ACTUAL PAGE NUMBERS ==="
    foreach ($p in $doc.Paragraphs) {
        $txt = $p.Range.Text.Trim()
        if ($txt -match "^(CHAPTER|ACKNOWLEDGEMENTS|EXECUTIVE SUMMARY|LIST OF|TABLE OF CONTENTS|CONCLUSION|[1-5]\.[0-9])") {
            $pageNo = $p.Range.Information(3) # 3 = wdActiveEndPageNumber
            Write-Host ("Page " + $pageNo + ": " + $txt)
        }
    }

    $doc.Close([ref]0)
} catch {
    Write-Host ("Error: " + $_.Exception.Message)
} finally {
    $word.Quit()
}

