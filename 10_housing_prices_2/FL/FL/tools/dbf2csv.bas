Attribute VB_Name = "dbf2csv"
Sub FindFiles()
Dim strDocPath As String
Dim strCurrentFile As String
Dim Fname As String
Application.ScreenUpdating = False

strDocPath = "C:\Users\adria\github\BountyScrapers\10_housing_prices_2\FL\FL\DBF\"
'strCurrentFile = Dir(strDocPath & "*.*")
strCurrentFile = Dir(strDocPath & "*.dbf")

Do While strCurrentFile <> ""

    Workbooks.Open Filename:=strDocPath & strCurrentFile
    Fname = Left$(strCurrentFile, Len(strCurrentFile) - 4) & ".csv"
    ActiveWorkbook.SaveAs Filename:=strDocPath & "csv\" & Fname, FileFormat:=xlCSV, CreateBackup:=False
    ActiveWorkbook.Close (False)
strCurrentFile = Dir
Loop
Application.ScreenUpdating = True
End Sub
