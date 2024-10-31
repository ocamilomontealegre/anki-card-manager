from pathlib import Path
from fastapi import UploadFile
from pandas import read_csv, DataFrame
from common.utils.file_utils import FileUtils


class FileService:
    def __init__(self):
        pass

    async def __save_uploaded_file(self, file_path: Path, file_data: UploadFile) -> Path:
        with open(file_path, "wb") as file:
            file.write(await file_data.read())
        return file_path

    async def process_file(self, file: UploadFile):
        file_path = FileUtils.create_folder("uploads") / file.filename
        file_name = await self.__save_uploaded_file(file_path, file)
        df: DataFrame = read_csv(file_name, delimiter=";")
        for _, row in df.iterrows():
            print(row["word"])