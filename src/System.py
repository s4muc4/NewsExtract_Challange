import zipfile
import os

class SystemOperations():
    def __init__(self) -> None:
        self.folder_path = "output/pictures"

    def archive_pictures(self):

        folder_path = self.folder_path
        output_filename = f"{self.folder_path}.zip"

        with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, os.path.dirname(folder_path)))
