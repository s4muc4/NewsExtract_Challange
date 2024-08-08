from src.Sheets import Sheets_Manipulation

title = "result"
sheet_name = "Olympics"

sheet = Sheets_Manipulation(title=title)

sheet.create_file()
sheet.create_worksheet(sheet_name)
sheet.add_row_in_worksheet(sheet_name, ["taoo", "teste2", "teste3", "teste4", "teste5", "teste6"])