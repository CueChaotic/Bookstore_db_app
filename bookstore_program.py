# ***** P's BOOKS DATABASE SYSTEM *****

# ===== IMPORTS =====
import sqlite3
from tabulate import tabulate

# ===== FUNCTIONS =====

def numeric_check(entry):
    '''
    Checks that string input is strictly numerical.
    If FALSE - Prints a prompt to re-enter digits only
    '''
    while entry.isnumeric() == False:
        entry = input('''
Please enter only digits:
: ''')
    return entry


def db_checker():
    '''
    Checks that the "book" TABLE exists AND contains any entries. If not, menu
    option is disallowed and user is prompted to first create a new entry.
    '''
    db = sqlite3.connect("ebookstore.db")
    cursor = db.cursor()
    try:
        # Check if the TABLE contains any entries; redirect user if None.
        cursor.execute('''SELECT id FROM book WHERE id = ?''', (3001,))
        result = cursor.fetchone()
        if result is None:
            print('''
___________________________________________________________

NO DATA EXISTS -- PLEASE CREATE A NEW ENTRY FIRST
___________________________________________________________''')
            return False
        else:
            return True
    # Account for the case where the TABLE itself does not exist.
    except sqlite3.OperationalError as ex:
        if "no such table" in str(ex):  # Check for the "no such table" string
            print('''
___________________________________________________________

NO DATA EXISTS -- PLEASE CREATE A NEW ENTRY FIRST
___________________________________________________________''')
            return False
    finally:
        db.close()


def db_builder():
    '''
    Creates (or, if already exists, opens) the "book" TABLE with automatic ID
    number sequencing.
    '''
    db = sqlite3.connect("ebookstore.db")
    cursor = db.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS
                        book(id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT,
                        author TEXT,
                        qty INTEGER);''')
    # Check if the table is new by querying the sqlite_sequence table.
    cursor.execute('''SELECT seq FROM sqlite_sequence 
                   WHERE name = 'book';''')
    result = cursor.fetchone()
    # If table new, start initial value of the ID column from 3001.
    if result is None:
        cursor.execute('''INSERT INTO sqlite_sequence (name, seq)
                          VALUES ('book', 3000);''') # Insert 3000 to start count from 3001.
    db.commit()
    db.close()

    # NOTE: The idea and understanding for the sqlite_sequence table and 
    # AUTOINCREMENT command was taken from user iTech at Stackoverflow:
    # https://stackoverflow.com/questions/692856/set-start-value-for-autoincrement-in-sqlite
    # in order to provide an efficient method for insertion of the book IDs
    # and eliminate the likelihood of user input error.


def db_display_all():
    '''
    Retrieves all book records and prints them in a table.
    '''
    # Capture book records in a list for tabulation.
    data_table = [('ID', 'Title', 'Author', 'Qty')]
    db = sqlite3.connect("ebookstore.db")
    cursor = db.cursor()
    cursor.execute('''SELECT id, title, author, qty
                   FROM book''')
    results = cursor.fetchall()
    for row in results:
        data_table.append(row)
    print('''
DISPLAYING ALL BOOKS
(excludes deleted records)
''')
    # Print the table using the tabulate module.
    print(tabulate(data_table, headers = 'firstrow', tablefmt = 'fancy_grid'))
    db.close()


def db_grabber(id):
    '''
    Retrieves a specified book record by reference to ID.
    '''
    db = sqlite3.connect("ebookstore.db")
    cursor = db.cursor()
    cursor.execute('''SELECT id, title, author, qty
                   FROM book
                   WHERE id = ?''', (id, ))
    result = cursor.fetchone()
    # Inform user if the ID does not exist.
    if result is None:
        print('''
___________________________________________________________

BOOK ID NOT FOUND
___________________________________________________________''')
    db.close()
    return result


def db_new_entry(title, author, qty):
    '''
    Captures a new record into the TABLE "book" in the DATABASE "ebookstore'.
    '''
    db = sqlite3.connect("ebookstore.db")
    cursor = db.cursor()
    cursor.execute('''INSERT INTO book(title, author, qty)
                   VALUES (?, ?, ?)''', (title, author, qty))
    db.commit()
    db.close()
    # Inform user of successful entry.
    print('''
___________________________________________________________

NEW BOOK ADDED!
___________________________________________________________''')


def db_book_update(id, title, author, qty):
    '''
    Updates existing record in the TABLE "book" in the DATABASE "ebookstore'.
    '''
    db = sqlite3.connect("ebookstore.db")
    cursor = db.cursor()
    cursor.execute('''UPDATE book
                      SET title = ?, author = ?, qty = ?
                      WHERE id = ?''', (title, author, qty, id))
    db.commit()
    db.close()
    # Inform user of successful update.
    print('''
___________________________________________________________

BOOK UPDATED!
___________________________________________________________''')


def db_book_deletion(id):
    '''
    Deletes selected book record from the TABLE "book" in the DATABASE
    "ebookstore".
    '''
    db = sqlite3.connect("ebookstore.db")
    cursor = db.cursor()
    cursor.execute('''SELECT id, title, author, qty 
                    FROM book
                    WHERE id = ?''', (id, ))
    result = cursor.fetchone()
    if result is None:
        print('''
___________________________________________________________

BOOK ID NOT FOUND
___________________________________________________________''')
    # Confirm deletion with user first.
    else:
        confirmation = input(f'''
Are you sure you want to delete book with ID {result[0]}?

Title:  {result[1]}
Author: {result[2]}
Qty:    {result[3]}

[Indicate y (Yes) or n (No)]
: ''').lower()
        while confirmation not in ['y', 'n']:
            confirmation = input(f'''
Invalid entry. Indicate y (Yes) or n (No)
: ''').lower()
        # Execute deletion if confirmed YES.
        if confirmation == 'y':
            cursor.execute('''DELETE FROM book
                            WHERE id = ?''', (id, ))
            db.commit()
            print(f'''
___________________________________________________________

BOOK WITH ID -- {id} -- DELETED!
___________________________________________________________''')
        # Cancel deletion if confirmed NO.
        elif confirmation == 'n':
            print('''
___________________________________________________________

OPERATION CANCELLED
___________________________________________________________''')
    db.close()


# ===== THE PROGRAM =====

# In all options besides the ENTER BOOK and EXIT options, the program will
# check if the "book" TABLE exists and contains any entries, via the
# db_checker function. If not, the user will be prompted to first create a new
# entry in each case.

while True:
    
    # MENU SELECTION
    menu_select = input('''
==========================================================

        +++++++++ eBOOK DATABASE +++++++++

==========================================================

    MENU
                        
        PRESS (1) Enter Book
        
        PRESS (2) Update Book
                        
        PRESS (3) Delete Book
                        
        PRESS (4) Search Books
                        
    EXIT (e)
___________________________________________________________

: ''').lower()
    
    # NEW BOOK ENTRY
    if menu_select == "1":
        while True:
            book_entry = input('''
___________________________________________________________

NEW BOOK ENTRY
                
Press "f" to proceed to book entry.
Press "e" to go back to the Main Menu.
___________________________________________________________

: ''').lower()

            if book_entry == "e":
                break
            # Enter new book details
            elif book_entry == "f":
                enter_title = input('''
Please enter the title of the book to be added:
: ''')
                enter_author = input('''
Please enter the author of the book to be added:
: ''')
                enter_qty = input('''
Please enter quantity of books to be added:
: ''')
                enter_qty = numeric_check(enter_qty)
                # Confirm details with user before saving
                while True:
                    entry_confirmation = input(f'''
Are you happy with the below details?
___________________________________________________________

NEW BOOK ENTRY
                                           
Title:              {enter_title}
                    [To edit: Press "1"]

Author:             {enter_author}
                    [To edit: Press "2"]

Quantity in stock:  {enter_qty}
                    [To edit: Press "3"]
                
Press "y" to save details
Press "n" to cancel entry
___________________________________________________________
                                           
: ''').lower()
                    # Check for valid input first
                    while entry_confirmation not in ['1', '2', '3',
                                                    'y', 'n']:
                        entry_confirmation = input('''
Please enter a valid option:
: ''').lower()                 
                    # Save details to database if confirmed YES
                    if entry_confirmation == "y":
                        db_builder()
                        db_new_entry(enter_title, enter_author, int(enter_qty))
                        break

                    elif entry_confirmation == "n":
                        break
                    
                    elif entry_confirmation == "1":
                        enter_title = input('''
Edit title:
: ''')
                        continue # Returns to the confirmation prompt

                    elif entry_confirmation == "2":
                        enter_author = input('''
Edit author:
: ''')
                        continue

                    elif entry_confirmation == "3":
                        enter_qty = input('''
Edit quantity:
: ''')
                        enter_qty = numeric_check(enter_qty)
                        continue

            else:
                print('''
PLEASE ENTER A VALID OPTION FROM THE MENU''')
    
    # BOOK UPDATE OPTION
    if menu_select == "2":
        # Run the db_checker function to ensure the TABLE exists.
        if db_checker() == False:
            continue
        while True:
            book_update = input('''
___________________________________________________________

BOOK UPDATE
                
Press "f" to proceed to book update.
Press "e" to go back to the Main Menu.
___________________________________________________________

:''').lower()

            if book_update == "e":
                break

            # Run the book search function and retrieve all details.
            elif book_update == "f":
                id_update_prompt = input('''
Please enter the ID of the book you'd like to update
: ''')
                id_update_prompt = numeric_check(id_update_prompt)
                data_retrieval = db_grabber(int(id_update_prompt))
                if data_retrieval is None:
                    continue                
                # Capture the retrieved data for editing.
                id_retrieval = data_retrieval[0]
                title_retrieval = data_retrieval[1]
                author_retrieval = data_retrieval[2]
                qty_retrieval = data_retrieval[3]
                while True:
                    update_prompt = input(f'''
___________________________________________________________

EDITING BOOK ENTRY

ID No. {id_retrieval}

Title:              {title_retrieval}
                    [To edit: Press "1"]

Author:             {author_retrieval}
                    [To edit: Press "2"]

Quantity in stock:  {qty_retrieval}
                    [To edit: Press "3"]
                
Press "y" to save details
Press "n" to cancel entry
___________________________________________________________

: ''').lower()
                    while update_prompt not in ['1', '2', '3',
                                                'y', 'n']:
                        update_prompt = input('''
Please enter a valid option:
: ''').lower()

                    if update_prompt == "1":
                        title_retrieval = input('''
Edit title:
: ''')
                        print('''
CONFIRM DETAILS BELOW''')
                        continue

                    elif update_prompt == "2":
                        author_retrieval = input('''
Edit author:
: ''')
                        print('''
CONFIRM DETAILS BELOW''')
                        continue

                    elif update_prompt == "3":
                        qty_retrieval = input('''
Edit quantity:
: ''')
                        qty_retrieval = numeric_check(qty_retrieval)
                        print('''
CONFIRM DETAILS BELOW''')
                        continue

                    # Run the UPDATE function if confirmed YES
                    elif update_prompt == "y":
                        db_book_update(id_retrieval, title_retrieval,
                                       author_retrieval, qty_retrieval)
                        break

                    elif update_prompt == "n":
                        break

            else:
                print('''
PLEASE ENTER A VALID OPTION FROM THE MENU''')
    
    # BOOK DELETION

    # A note when books are deleted: The ID sequence will not be renumbered.
    # The ID numbers will continue to increment from the last number used.
    # This is usually also relevant from an audit trail perspective, where the
    # history of the database is maintained.

    elif menu_select == "3":
        if db_checker() == False:
            continue
        while True:
            book_delete = input('''
___________________________________________________________

BOOK DELETION
                
Press "f" to proceed to book deletion.
Press "e" to go back to the Main Menu.
___________________________________________________________

:''').lower()

            if book_delete == "e":
                break

            # Runs the book deletion function
            elif book_delete == "f":
                book_id = input('''
Please enter the ID of the book to be deleted:
: ''')
                book_id = numeric_check(book_id)
                db_book_deletion(int(book_id))

            else:
                print('''
PLEASE ENTER A VALID OPTION FROM THE MENU''')

    # BOOK SEARCH
    elif menu_select == "4":
        if db_checker() == False:
            continue
        while True:
            book_search = input('''
___________________________________________________________

BOOK SEARCH
                
Press "d" to display all books.
Press "f" to search for a book.
Press "e" to go back to the Main Menu.
___________________________________________________________

:''').lower()
        
            if book_search == "e":
                break

            # Run the book search function and retrieve all details.
            elif book_search == "f":        
                id_search_prompt = input('''
Please enter the ID of the book you'd like to search
: ''')
                id_search_prompt = numeric_check(id_search_prompt)
                search_retrieval = db_grabber(int(id_search_prompt))
                if search_retrieval is None:
                    continue                
                id_search = search_retrieval[0]
                title_search = search_retrieval[1]
                author_search = search_retrieval[2]
                qty_search = search_retrieval[3]
                print(f'''
___________________________________________________________

BOOK DETAILS

ID No. {id_search}

Title:              {title_search}

Author:             {author_search}

Quantity in stock:  {qty_search}   
___________________________________________________________''')

            elif book_search == "d":
                db_display_all()

            else:
                print('''
PLEASE ENTER A VALID OPTION FROM THE MENU''')

    # EXIT PROGRAM
    elif menu_select == "e":
        print('''
___________________________________________________________

YOU HAVE BEEN LOGGED OUT
___________________________________________________________
''')
        exit()

    else:
        print('''
PLEASE ENTER A VALID OPTION FROM THE MENU''')
        
