from wind32com import client

excel = client.Dispatch("Excel.Application")
excel.Visable = True
wb = excel.Workbooks.Add()
ws = wb.Worksheets.Add()
ws.Name = "My Worksheet"
ws.Range("A1:B10").Value = "Hello World!"
ws.SaveAs("C:\\Users\\USERNAME\\Desktop\\HelloExcel.xlsx")
excel.Application.Quit()