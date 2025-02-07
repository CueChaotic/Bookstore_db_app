# Bookstore DB App

## Introduction

This is a simple database application for recording books in a bookstore, written in Python
and using SQLite for database management.

## Contents

1. Feature Overview
2. Installation
3. Usage
4. Credits

## 1. Feature Overview

Consists of the following functionality:
* Entering new book details:
  * Title
  * Author
  * Quantity
* Updating existing book details
* Book deletion
* Book search
* Exit functionality

## 2. Installation

Compatible with:
* Windows
* MacOS
* Linux-based OS

2.1 Ensure you already have a Python interpreter installed. You may download it from [here](https://www.python.org/downloads/).

2.2 Open the Command Terminal relevant to your operating system and navigate to the directory
you would like to use for the app files:
* For Windows, this can either be Command Prompt or Windows PowerShell.
* For MacOS and Linux, this will be Bash.

2.3 Clone this Git repository to your chosen local directory by running this command in your
terminal:
   
    git clone https://github.com/CueChaotic/Bookstore_db_app.git

2.4 A new directory called **Bookstore_db_app** should now appear within your current directory.

2.5 Set up and activate a Virtual Environment as follows:

* For **Windows** systems, enter the below command in your terminal, in the current directory:
    ```
    python -m venv projenv
    ```
* For **MacOS** and **Linux** systems, enter the below:
    ```
    python3 -m venv projenv
    ```
This will create a virtual environment directory called "projenv".

* Activate your virtual environment as follows, depending on your terminal:
    * **Command Prompt (Windows)**:
        ```
        projenv\scripts\activate
        ```
    * **Windows PowerShell (Windows)**:
        ```
        .\projenv\scripts\activate
        ```
    * **Bash (MacOS and Linux)**:
        ```
        source projenv/bin/activate
        ```
    Your environment should now be activated.

    **NOTE**: The virtual env needs to be active as it contains the necessary module(s) to run the
    program. Once you are finished running the program, you can deactivate the virtual env by
    running the below in your terminal:
        ```
        deactivate
        ```

2.6 Navigate into the Bookstore_db_app directory in your terminal:

    cd Bookstore_db_app

2.7 Run the below command to install dependencies:

    pip install -r requirements.txt

## 3. Usage

Run the below command in your terminal to initiate the program but ensure your virtual environment
is activated beforehand (as laid out above):
```
python Bookstore_program.py
```

**Note**: Use python3 if on Linux or MacOS

## 4. Credits

Built by CueChaotic
