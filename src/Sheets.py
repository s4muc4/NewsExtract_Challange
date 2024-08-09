
from RPA.Excel.Files import Files
from datetime import datetime
import os

class Sheets_Manipulation():
    def __init__(self) -> None:
        """Initializing class of sheets"""
        current_date = datetime.now().strftime("%d_%m_%Y")
        title = f"result_{current_date}"
        self.file = Files()
        self.title = title
        self.path = f"output/news_{title}.xlsx"

    def create_file(self):
        if not os.path.exists(self.path):
            print("file doesn't exists, creating")
            self.file.create_workbook(sheet_name="Sheet1")
            columns = ["Empty"]
            self.file.append_rows_to_worksheet(name="Sheet1", content=[columns])
            self.file.save_workbook(path=self.path)
        else:
            print("file exists")

    def create_worksheet(self, sheet):
        self.file.open_workbook(self.path)
        if not self.file.worksheet_exists(sheet):
            print("criando worksheet " + sheet)
            self.file.create_worksheet(sheet)
            columns = ["Title", "Topic", "Date", "Description", "Picture_Source", "Title_Words", "Description_Words", "Money_Contains", "URL"]
            self.file.append_rows_to_worksheet(name=sheet, content=[columns])
        self.file.save_workbook(path=self.path)

    def add_row_in_worksheet(self,sheet,row):
        self.file.open_workbook(self.path)
        self.delete_worksheet_if_exists("Sheet1")
        columns = row
        self.file.append_rows_to_worksheet(name=sheet, content=[columns])
        self.file.save_workbook(path=self.path)

    def delete_worksheet_if_exists(self, sheet):
        try:
            if len(self.file.list_worksheets())==1:
                self.create_worksheet("Sheet1")
            if self.file.worksheet_exists(sheet):
                self.file.remove_worksheet(sheet)
        except Exception as err:
            self.file.open_workbook(self.path)
            if len(self.file.list_worksheets())==1:
                self.create_worksheet("Sheet1")
            if self.file.worksheet_exists(sheet):
                self.file.remove_worksheet(sheet)
            self.file.save_workbook(path=self.path)
