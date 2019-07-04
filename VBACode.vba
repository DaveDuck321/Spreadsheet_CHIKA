Sub FillBlack(width, height)
    Sheets("Canvas").Activate
    Range("A1:" & Cells(height + 1, width + 1).Address).Interior.color = 0
End Sub

Sub FillImage()
    Sheets("CodeOutput").Activate
    Dim meta() As Variant
    Dim data() As Variant
    meta = Range("A1:D1")
    data = Range(meta(1, 3))
    imageWidth = meta(1, 1)
    imageHeight = meta(1, 2)
    Sheets("Canvas").Activate
    
    Call FillBlack(imageWidth, imageHeight)
    
    Count = 0
    Application.ScreenUpdating = False
    For dataY = 1 To UBound(data, 1)
        For dataX = 1 To UBound(data, 2)
            If Int(data(dataY, dataX)) > 0 Then
                imageX = Count Mod imageWidth
                imageY = Int(Count / imageWidth)
                Cells(imageY + 1, imageX + 1).Interior.color = data(dataY, dataX)
            ElseIf data(dataY, dataX) = "" Then
                Exit For
            End If
            Count = Count + 1
        Next dataX
        DoEvents
    Next dataY
    Application.ScreenUpdating = True
End Sub

Sub FillVideo()
    Call FillImage
    
    Sheets("CodeOutput").Activate
    Dim meta() As Variant
    Dim data() As Variant
    meta = Range("A1:D1")
    data = Range(meta(1, 4))
    frameWidth = meta(1, 1)
    frameHeight = meta(1, 2)
    Sheets("Canvas").Activate
    For frame = 1 To UBound(data, 1)
        Application.ScreenUpdating = False
        For diff = 1 To UBound(data, 2) Step 2
            pos = data(frame, diff)
            If pos = "" Then
                Exit For
            End If
            Cells(Int(pos / frameWidth) + 1, (pos Mod frameWidth) + 1).Interior.color = data(frame, diff + 1)
        Next diff
        Application.ScreenUpdating = True
        DoEvents
    Next frame
End Sub
