import sys
from abc import ABC, abstractmethod
from copy import deepcopy
from datetime import datetime
from typing import Optional, Union

from config import ROWS_COUNT_IN_PAGE
from data import CSVDataManager

data_manager = CSVDataManager(file_name='contacts')


class Command(ABC):
    @abstractmethod
    def execute(self, data: Union[dict, str, None]):
        raise NotImplementedError('Commands must implement an execute method')


class AddContactCommand(Command):
    def execute(self,
                data: dict[str, str],
                timestamp: Optional[str] = None,
                ) -> tuple[bool, None]:

        data['date_added'] = timestamp or datetime.utcnow().isoformat()
        data_manager.add(data)
        return True, None


class ListContactsCommand(Command):
    order_by: Optional[str]
    row_slice: list[int, Optional[int]]

    def __init__(self, order_by=None):
        self.order_by = order_by
        self.row_slice = [0, ROWS_COUNT_IN_PAGE]

    def execute(self, data: Optional[dict[str, str]] = None) -> tuple[bool, list[dict[str]]]:
        return True, data_manager.list(data, order_by=self.order_by, row_slice=self.row_slice)


class DeleteContactCommand(Command):
    def execute(self, data: dict[str, str]) -> tuple[bool, None]:
        data_manager.delete(criteria=data)
        return True, None


class QuitCommand(Command):
    def execute(self, data: None = None) -> None:
        sys.exit()


class EditContactCommand(Command):
    def execute(self, data: dict[str, Union[dict, str]]) -> tuple[bool, None]:
        data_manager.update(criteria={'id': data['id']}, data=data['update'])
        return True, None


class QuitPageLoopCommand(Command):
    def execute(self, data: None) -> None:
        import main
        while True:
            main.main_loop()


def get_previous_page_command(command: ListContactsCommand) -> ListContactsCommand:
    """ Get the Command instance for getting previous page of contacts. """
    previous_page_command = deepcopy(command)
    if command.row_slice[0] >= ROWS_COUNT_IN_PAGE:
        previous_page_command.row_slice[0] -= ROWS_COUNT_IN_PAGE
        previous_page_command.row_slice[1] -= ROWS_COUNT_IN_PAGE
    else:
        previous_page_command.row_slice[0] = 0
        previous_page_command.row_slice[1] = ROWS_COUNT_IN_PAGE
    return previous_page_command


def get_next_page_command(command: ListContactsCommand) -> ListContactsCommand:
    """ Get the Command instance for getting next page of contacts. """
    list_length = len(data_manager.list())

    next_page_command = deepcopy(command)
    if command.row_slice[1] + ROWS_COUNT_IN_PAGE > list_length:
        next_page_command.row_slice[0] = list_length - ROWS_COUNT_IN_PAGE
        next_page_command.row_slice[1] = list_length
    else:
        next_page_command.row_slice[0] += ROWS_COUNT_IN_PAGE
        next_page_command.row_slice[1] += ROWS_COUNT_IN_PAGE
    return next_page_command
