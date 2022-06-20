from enum import Enum
from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from pykeyboard import InlineKeyboard, InlineButton


from database import BooksDatabase

api_id = 6
api_hash = "eb06d4abfb49dc3eeb1aeb98ae0f581e"


class State(Enum):
    NONE = ""

    SEARCH = "search"

    SEARCH_BOOK_TITLE = "search_title"
    SEARCH_BOOK_AUTHOR = "search_author"
    SEARCH_BOOK_DESCRIPTION = "search_description"
    SEARCH_BOOK_NOTES = "search_notes"

    PAGINATOR = "paginator"

    DETAILED_BOOK_INFO = "detailed_book_info"

    ADD_NOTE = "add_note"


STATE = State.NONE


app = Client(
    "Bot",
    api_id=api_id,
    api_hash=api_hash,
    bot_token="5313059421:AAEHlVfKWG-DiPS5krh3LToqR_YlNkytfdo",
)
database = BooksDatabase()

FOUND = []
INDEX = 0
CURRENT_BOOK = {}


@app.on_message(filters.private & filters.command("start"))
async def begin(client: Client, message: Message):
    button = [[InlineKeyboardButton("Search", callback_data="search")]]
    await message.reply_text(
        "Click search to search", reply_markup=InlineKeyboardMarkup(button)
    )


@app.on_message(filters.private)
async def parse(client: Client, message: Message):
    global STATE, FOUND, CURRENT_BOOK, INDEX

    match STATE:
        case State.SEARCH_BOOK_TITLE:
            query = message.text
            FOUND = list(database.find_book(query, database.TITLE))

        case State.SEARCH_BOOK_AUTHOR:
            query = message.text
            FOUND = list(database.find_book(query, database.AUTHOR))

        case State.SEARCH_BOOK_DESCRIPTION:
            query = message.text
            FOUND = list(database.find_book(query, database.DESCRIPTION))

        case State.SEARCH_BOOK_NOTES:
            query = message.text
            FOUND = list(database.find_book(query, database.NOTES))

        case STATE.ADD_NOTE:
            query = message.text
            res = database.insert_note(CURRENT_BOOK["title"], query)
            if not res:
                await message.reply_text("Failed to add note")
                return

    if STATE in [
        State.SEARCH_BOOK_TITLE,
        State.SEARCH_BOOK_AUTHOR,
        State.SEARCH_BOOK_DESCRIPTION,
        State.SEARCH_BOOK_NOTES,
    ]:
        CURRENT_BOOK = FOUND[0]
        INDEX = 0
        STATE = State.PAGINATOR
        keyboard = InlineKeyboard()
        keyboard.paginate(len(FOUND), INDEX + 1, "pagination_keyboard:{number}")
        keyboard.row(
            InlineButton("Detailed Book Info", "pagination_detail"),
            InlineButton("Add a Note", "add_note"),
        )
        await message.reply_text(f"{CURRENT_BOOK.get('title')}", reply_markup=keyboard)
    elif STATE == State.ADD_NOTE:
        keyboard = InlineKeyboard()
        keyboard.row(
            InlineButton("Back to Detailed Book Info", "pagination_detail"),
            InlineButton("Add another Note", "add_note"),
        )
        await message.reply_text(
            f"Your note ({query}) was added!", reply_markup=keyboard
        )


@app.on_callback_query()
async def callback_query(client: Client, callback_query: CallbackQuery):
    global STATE, FOUND, CURRENT_BOOK, INDEX

    match callback_query.data.split(":")[0]:
        case "search":
            markup = search_menu()
            await callback_query.message.edit(
                "Choose a method to search by", reply_markup=markup
            )
            STATE = State.SEARCH

        case "search_title":
            await callback_query.message.edit("Enter book title")
            STATE = State.SEARCH_BOOK_TITLE

        case "search_author":
            await callback_query.message.edit("Enter book author")
            STATE = State.SEARCH_BOOK_AUTHOR

        case "search_description":
            await callback_query.message.edit("Enter book description")
            STATE = State.SEARCH_BOOK_DESCRIPTION

        case "search_notes":
            await callback_query.message.edit("Enter book notes")
            STATE = State.SEARCH_BOOK_NOTES

        case "pagination_detail":
            book = CURRENT_BOOK
            book_str = f"""Title: {book.get("title")}"""

            if published_date := book.get("publishedDate"):
                book_str += f"""\nPublished Date: {published_date}"""
            if description := book.get("shortDescription"):
                book_str += f"""\nDescription: {description}"""
            if authors := book.get("author"):
                book_str += f"""\nAuthor: {", ".join(authors)}"""
            if categories := book.get("categories"):
                book_str += f"""\nCategories: {", ".join(categories)}"""
            if page_count := book.get("pageCount"):
                book_str += f"""\nPage Count: {page_count}"""
            if isbn := book.get("isbn"):
                book_str += f"""\nISBN: {isbn}"""

            keyboard = InlineKeyboard()
            keyboard.row(
                InlineButton("Add a Note", "add_note"),
                InlineButton("Back to Results", "back_results"),
            )

            if hasattr(book, "longDescription"):
                keyboard.row.add(InlineButton("Show more info", callback_data="more"))

            await callback_query.message.edit(book_str, reply_markup=keyboard)

        case "pagination_keyboard":
            INDEX = int(callback_query.data.split(":")[-1]) - 1
            CURRENT_BOOK = FOUND[INDEX]
            keyboard = InlineKeyboard()
            keyboard.paginate(len(FOUND), INDEX + 1, "pagination_keyboard:{number}")
            keyboard.row(
                InlineButton("Detailed Book Info", "pagination_detail"),
                InlineButton("Add a Note", "add_note"),
            )
            await callback_query.message.edit(
                f"{FOUND[int(callback_query.data.split(':')[1]) - 1].get('title')}",
                reply_markup=keyboard,
            )

        case "add_note":
            await callback_query.message.edit(
                f"Enter a note to insert for `{CURRENT_BOOK.get('title')}`"
            )
            STATE = State.ADD_NOTE

        case "back_results":
            keyboard = InlineKeyboard()
            keyboard.paginate(len(FOUND), INDEX + 1, "pagination_keyboard:{number}")
            keyboard.row(
                InlineButton("Detailed Book Info", "pagination_detail"),
                InlineButton("Add a Note", "add_note"),
            )
            await callback_query.message.edit(
                f"{FOUND[INDEX].get('title')}",
                reply_markup=keyboard,
            )

        case _:
            await callback_query.message.reply("Something went wrong")


def search_menu() -> InlineKeyboardMarkup:
    button = [
        [InlineKeyboardButton("By title", callback_data="search_title")],
        [InlineKeyboardButton("By author", callback_data="search_author")],
        [InlineKeyboardButton("By description", callback_data="search_description")],
        [InlineKeyboardButton("By notes", callback_data="search_notes")],
    ]
    return InlineKeyboardMarkup(button)


app.run()