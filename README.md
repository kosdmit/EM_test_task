# Contacts Manager

Contacts Manager is a simple command-line application for managing contacts. It allows users to add, edit, delete, and list contact information. Users can also search for contacts using multiple criteria queries.

### Requirements
- Python 3.9+

### Setup
- Clone this repository or download the source code to your local machine.

    ```shell
    git clone https://github.com/kosdmit/EM_test_task.git
    cd EM_test_task
    ```

### Run
- Run the main script to start the Contacts Manager.

    ```shell
    python main.py
    ```   
  
## Usage and Functionality
This program has command-line interface. The main menu includes follow six options:

### (A) Adding a Contact

1. Input sign 'A' to select the "Add Contact" option from the menu.
2. Enter the contact information as prompted, including the first name, last name, middle name (optional), work phone (optional), and personal phone.
3. The contact will be added to the list and assigned a unique ID.

### (L) Listing Contacts

1. Select the "List Contacts" option from the menu.
2. Contacts will be displayed in pages, with a configurable number of contacts per page (default is set in the config file).
3. You can navigate through the pages by selecting the "Next Page" or "Previous Page" options.
4. For quitting to main menu input 'Q' sign.

### (S) Searching for a Contact

1. Select the "Search Contacts" option from the menu.
2. Enter the search criteria, such as first name, last name, or phone number.
3. You can search by one and multiples fields. For multi criteria search split fields by comma.
4. Input search values for selected fields using the same sequence of fields and split values by comma.
5. Matching contacts will be displayed on the screen.

### (E) Editing a Contact

1. Select the "Edit Contact" option from the menu.
2. Enter the unique ID of the contact you want to edit.
3. Update the contact information as prompted.
4. The changes will be saved, and the updated contact information will be displayed.

### (D) Deleting a Contact

1. Select the "Delete Contact" option from the menu.
2. Enter the unique ID of the contact you want to delete.
3. The contact will be removed from the list.

### (Q) Quitting the Program

1. Select the "Quit" option from the menu to exit the Contacts Manager.

## Storage

Contacts Manager uses CSV file to handle storage and retrieval of contacts. All contacts are stored in a file named `contacts.csv` located in the same directory as the program. Each contact is assigned a unique ID and stored with its associated information, including the first name, last name, middle name (if provided), work phone, personal phone, and the date when the contact was added.

### CSV File Format

The `contacts.csv` file follows a specific format:

- The first row contains the column headers: `id`, `last_name`, `first_name`, `middle_name`, `work_phone`, `personal_phone`, `date_added`.
- Each subsequent row represents a contact and contains the corresponding data for each column.

## Disclaimer
This program is intended for job test task purpose.