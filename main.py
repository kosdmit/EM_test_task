#!/usr/bin/env python

import os
import re
import typing
from collections import OrderedDict
from typing import Optional, Callable, Union

import commands


def format_contact(contact: dict[str, str]) -> str:
    """ Formats a contact data into a tab-separated string for printing to console. """
    return '\t'.join(
        str(value) if value else ''
        for key, value in contact.items()
    )


class Option:
    """ Represents an option in the menu with associated command and callbacks. """
    name: str
    command: commands.Command
    prep_call: Optional[Callable]
    success_message: str
    after_call: Optional[Callable]

    def __init__(self, name, command, prep_call=None, success_message='{result}', after_call=None):
        self.name = name
        self.command = command
        self.prep_call = prep_call
        self.success_message = success_message
        self.after_call = after_call

    def choose(self):
        """ Executes the option command and triggers associated callbacks. """
        data = self.prep_call() if self.prep_call else None
        success, result = self.command.execute(data)

        formatted_result = ''

        if isinstance(result, list):
            for contact in result:
                formatted_result += '\n' + format_contact(contact)
        else:
            formatted_result = result

        if success:
            print(self.success_message.format(result=formatted_result))

        if self.after_call:
            self.after_call(command=self.command)

    def __str__(self):
        return self.name


def clear_screen() -> None:
    """ Clears the console. """
    clear = 'cls' if os.name == 'nt' else 'clear'
    os.system(clear)


def print_options(options: typing.OrderedDict[str, Option]) -> None:
    """ Prints the options menu to the console. """
    for shortcut, option in options.items():
        print(f'({shortcut}) {option}')
    print()


def option_choice_is_valid(choice: str, options: typing.OrderedDict[str, Option]) -> bool:
    """ Checks if a given choice is valid in the menu. """
    return choice in options or choice.upper() in options


def get_option_choice(options: typing.OrderedDict[str, Option]) -> Option:
    """ Prompts the user for a valid option choice. """
    choice = input('Choose an option: ')
    while not option_choice_is_valid(choice, options):
        print('Invalid choice')
        choice = input('Choose an option: ')
    return options[choice.upper()]


def get_user_input(label: str, required: bool = True) -> str:
    """ Prompts the user for input contact field value with printing the specified label. """
    value = input(f'{label}: ') or None
    while required and not value:
        value = input(f'{label}: ') or None
    return value


def get_new_contact_data() -> dict[str, str]:
    """ Gets the contact data for a new contact from the user. """
    return {
        'last_name': get_user_input('Last name'),
        'first_name': get_user_input('First name'),
        'middle_name': get_user_input('Middle name', required=False),
        'work_phone': get_user_input('Work phone', required=False),
        'personal_phone': get_user_input('Personal phone'),
    }


def get_contact_data_for_deletion() -> dict[str, str]:
    """ Gets the contact ID for deletion from the user. """
    row_id = get_user_input('Enter a contact ID to delete')
    return {'id': row_id}


def get_new_contact_info() -> dict[str, Union[str, dict]]:
    """ Gets the contact ID and field data for editing a contact from the user. """
    # TODO: add fields validation
    contact_id = get_user_input('Enter a contact ID to edit')
    field = get_user_input(
        f'Choose a field to edit {commands.data_manager.field_names}'
    )
    new_value = get_user_input(f'Enter the new value for {field}')
    return {
        'id': contact_id,
        'update': {field: new_value},
    }


def get_search_criteria() -> dict[str, str]:
    """ Gets the search criteria from the user. """
    field_list = get_user_input(
        f'Choose a fields for searching {commands.data_manager.field_names}, use "," for splitting'
    ).split(sep=',')
    field_list = [field_name.strip() for field_name in field_list]

    values_list = get_user_input('Input a values for searching, use "," for splitting fields').split(sep=',')
    values_list = [clean_query(value) for value in values_list]

    search_criteria = dict(zip(field_list, values_list))
    return search_criteria


def clean_query(query):
    """
    Cleans a search query by removing excess whitespace and quotes
    and converting to lowercase.
    """
    query = query.strip()
    query = re.sub(r'\s+', ' ', query)
    query = re.sub(r'"', '', query)
    query = query.casefold()
    return query


def main_loop() -> None:
    """
    The main loop of the application that displays the options menu
    and handles user input.
    """
    clear_screen()

    options = OrderedDict({
        'A': Option(
            'Add a contact',
            commands.AddContactCommand(),
            prep_call=get_new_contact_data,
            success_message='Contact added!',
        ),
        'L': Option(
            'List contacts',
            commands.ListContactsCommand(),
            after_call=pages_loop,
        ),
        'S': Option(
            'Search contacts',
            commands.ListContactsCommand(),
            prep_call=get_search_criteria,
            success_message='{result}',
        ),
        'E': Option(
            'Edit a contact',
            commands.EditContactCommand(),
            prep_call=get_new_contact_info,
            success_message='Contact updated!'
        ),
        'D': Option(
            'Delete a contact',
            commands.DeleteContactCommand(),
            prep_call=get_contact_data_for_deletion,
            success_message='Contact deleted!',
        ),
        'Q': Option(
            'Quit',
            commands.QuitCommand()
        ),
    })
    print_options(options)

    chosen_option = get_option_choice(options)
    clear_screen()
    chosen_option.choose()

    _ = input('Press ENTER to return to menu')


def pages_loop(command: commands.ListContactsCommand) -> None:
    """ Handles the pagination loop for listing contacts. """
    previous_page_command = commands.get_previous_page_command(command)
    next_page_command = commands.get_next_page_command(command)

    options = OrderedDict({
        'P': Option(
            'Previous page',
            previous_page_command,
            after_call=pages_loop,
            success_message='{result}'
        ),
        'N': Option(
            'Next page',
            next_page_command,
            after_call=pages_loop,
            success_message='{result}'
        ),
        'Q': Option(
            'Quit',
            commands.QuitPageLoopCommand()
        ),
    })
    print_options(options)

    chosen_option = get_option_choice(options)
    clear_screen()
    chosen_option.choose()


if __name__ == '__main__':
    while True:
        main_loop()
