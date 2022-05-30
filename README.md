# **Telegram Bot for interacting with a mock database of books as a proof of concept**

## This is a work in progress, books are scientific and programmatic and have Russian tags to them. 
</br>

## **The database is meant to be locally hosted by design, as shown by the URI attribute of the BooksDatabase class.**
</br>

# Setup

## There are two files that must be created by the user, .token and .credentials
</br>

## The .token file is a text file containing the bot token with no quotes or extra whitespace, which is used to authenticate the bot, fill in the .token-example with just the bot token.
## The .credentials file is a text file containing the username and password for the database, fill in the .credentials-example file and rename to .credentials.
</br>

# Running

## The executable file on posix-like systems is main.py, simply run as ./main.py in a term. For windows, python3 main.py