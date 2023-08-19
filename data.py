import csv
import os
from abc import ABC, abstractmethod
from itertools import islice
from typing import Optional, List


class DataManager(ABC):
    @abstractmethod
    def create_table(self, columns: list[str]) -> None:
        raise NotImplementedError(
            'Data Manager must implement a create_table method')

    @abstractmethod
    def drop_table(self) -> None:
        raise NotImplementedError(
            'Data Manager must implement a drop_table method')

    @abstractmethod
    def add(self, data: dict[str, str]) -> None:
        raise NotImplementedError(
            'Data Manager must implement an add method')

    @abstractmethod
    def delete(self, criteria: dict[str, str]) -> None:
        raise NotImplementedError(
            'Data Manager must implement a delete method')

    @abstractmethod
    def list(self,
             criteria: Optional[dict[str, str]] = None,
             order_by: str = None,
             row_slice: Optional[list[int, Optional[int]]] = None,
             ) -> list[dict[str, str]]:

        raise NotImplementedError(
            'Data Manger must implement a select method')

    @abstractmethod
    def update(self,
               criteria: dict[str, str],
               data: dict[str, str],
               ) -> None:

        raise NotImplementedError(
            'Data Manger must implement an update method')


class CSVDataManager(DataManager):
    """
    Data manager that uses CSV files for storage.
    Receives file_name for creating csv file.
    """
    file_name: str
    field_names: Optional[list[str]]

    def __init__(self, file_name):
        self.file_name = file_name + '.csv'
        self.field_names = self._get_field_names()

        self.create_table(columns=[
            'id',
            'last_name',
            'first_name',
            'middle_name',
            'work_phone',
            'personal_phone',
            'date_added',
        ])


    def create_table(self, columns: list[str]) -> None:
        """ Create a new csv file with the specified columns. """
        if not self.field_names:
            with open(self.file_name, newline='', mode='w') as file:
                writer = csv.writer(file)
                writer.writerow(columns)
                self.field_names = columns


    def drop_table(self) -> None:
        """ Remove the current csv file. """
        if os.path.exists(self.file_name):
            os.remove(self.file_name)
            self.field_names = None


    def add(self, data: dict[str, str]) -> None:
        """ Add a new row to the table. """
        if not self.field_names:
            raise Exception("Table does not exist. Use create_table() first.")

        data['id'] = str(self._get_last_id() + 1)

        with open(self.file_name, newline='', mode='a') as file:
            writer = csv.DictWriter(file, fieldnames=self.field_names)
            writer.writerow(data)


    def delete(self, criteria: dict[str, str]) -> None:
        """ Delete rows from the table that match the specified criteria. """
        records = self.list()
        records = [row for row in records if not all(
            row[key] == value for key, value in criteria.items())]
        self._overwrite_with(records)


    def list(self,
             criteria: Optional[dict[str, str]] = None,
             order_by: Optional[str] = None,
             row_slice: Optional[list[int, Optional[int]]] = None,
             ) -> list[dict[str, str]]:
        """ List rows from the table that match the specified criteria. """

        with open(self.file_name, newline='', mode='r') as file:
            reader = csv.DictReader(file)

            records = [row for row in reader]

            if criteria:
                records = [
                    row for row in records
                    if all(row[key].lower() == value.lower() for key, value in criteria.items())
                ]

            if order_by:
                records = sorted(records, key=lambda row: row[order_by])

            if row_slice:
                page_records = []
                start_index = row_slice[0]
                end_index = row_slice[1]
                for row in islice(records, start_index, end_index):
                    page_records.append(row)
                return page_records

            return records


    def update(self,
               criteria: dict[str, str],
               data: dict[str, str],
               ) -> None:
        """ Update rows in the table that match the specified criteria. """

        records = self.list()
        for row in records:
            if all(row[key] == value for key, value in criteria.items()):
                for key, value in data.items():
                    row[key] = value
        self._overwrite_with(records)


    def _overwrite_with(self, records: List[dict[str, str]]) -> None:
        with open(self.file_name, newline='', mode='w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.field_names)
            writer.writeheader()
            for record in records:
                writer.writerow(record)


    def _get_field_names(self) -> Optional[str]:
        if not os.path.exists(self.file_name):
            return None
        with open(self.file_name, newline='', mode='r') as file:
            reader = csv.reader(file)
            return next(reader, None)


    def _get_last_id(self) -> int:
        last_id = 0
        with open(self.file_name, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                last_id = int(row['id'])
        return last_id
