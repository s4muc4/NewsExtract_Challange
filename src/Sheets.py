
from RPA.Excel.Files import Files
import os

class Sheets_Manipulation():
    def __init__(self, title) -> None:
        self.file = Files()
        self.title = title
        self.path = f"output/news_{title}.xlsx"


    def create_file(self):
        if not os.path.exists(self.path):
            print("file doesn't exists")
            self.file.create_workbook(sheet_name="Sheet1")
            self.file.save_workbook(path=self.path)
        else:
            print("file exists")

    def create_worksheet(self, sheet):

        self.file.open_workbook(self.path)
        if not self.file.worksheet_exists(sheet):
            self.file.create_worksheet(name=sheet)
            columns = ["Title", "Date", "Description", "Picture_Source", "Title_Words", "Description_Words", "Money_Contains", "URL"]
            self.file.append_rows_to_worksheet(name=sheet, content=[columns])
        if self.file.worksheet_exists("Sheet1"):
            self.file.remove_worksheet("Sheet1")
        self.file.save_workbook(path=self.path)

        

    def add_line_in_worksheet(self,sheet,row):
        self.file.open_workbook(self.path)
        columns = row
        self.file.append_rows_to_worksheet(name=sheet, content=[columns])
        self.file.save_workbook(path=self.path)