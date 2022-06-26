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
    bot_token=open(".token", "r"),
)
database = BooksDatabase()

FOUND = []
INDEX = 0
CURRENT_BOOK = {}


@app.on_message(filters.private & filters.command("start"))
async def begin(client: Client, message: Message):
    button = [[InlineKeyboardButton("Начать поиск", callback_data="search")]]
    await message.reply_text(
        "Для начала взаимодействия с архивом нажмите кнопку «Начать поиск»", reply_markup=InlineKeyboardMarkup(button)
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
                await message.reply_text("Ошибка при добавлении заметки")
                return
    if len(FOUND) == 0:
        return await message.reply_text("Ничего не найдено, попробуйте другой запрос")


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
            InlineButton("Детальная информация о книге", "pagination_detail"),
            InlineButton("Добавить заметку", "add_note"),
        )
        await message.reply_text(f"{CURRENT_BOOK.get('title')}", reply_markup=keyboard)
    elif STATE == State.ADD_NOTE:
        keyboard = InlineKeyboard()
        keyboard.row(
            InlineButton("Вернуться к детальной информации о книге", "pagination_detail"),
            InlineButton("Добавить другую заметку", "add_note"),
        )
        await message.reply_text(
            f"Ваша заметка ({query}) была успешно добавлена!", reply_markup=keyboard
        )


@app.on_callback_query()
async def callback_query(client: Client, callback_query: CallbackQuery):
    global STATE, FOUND, CURRENT_BOOK, INDEX

    match callback_query.data.split(":")[0]:
        case "search":
            markup = search_menu()
            await callback_query.message.edit(
                "Выберите метод поиска книги", reply_markup=markup
            )
            STATE = State.SEARCH

        case "search_title":
            await callback_query.message.edit("Введите название книги")
            STATE = State.SEARCH_BOOK_TITLE

        case "search_author":
            await callback_query.message.edit("Введите автора книги")
            STATE = State.SEARCH_BOOK_AUTHOR

        case "search_description":
            await callback_query.message.edit("Введите описание книги")
            STATE = State.SEARCH_BOOK_DESCRIPTION

        case "search_notes":
            await callback_query.message.edit("Введите ключевые слова из заметки")
            STATE = State.SEARCH_BOOK_NOTES

        case "pagination_detail":
            book = CURRENT_BOOK
            book_str = f"""<b>Название</b>: {book.get("title")}"""

            if published_date := book.get("publishedDate"):
                book_str += f"""\n<b>Дата публикации</b>: {published_date}"""
            if description := book.get("shortDescription"):
                book_str += f"""\n<b>Описание</b>: {description}"""
            if authors := book.get("authors"):
                book_str += f"""\n<b>Автор(ы)</b>: {", ".join(authors)}"""
            if categories := book.get("categories"):
                book_str += f"""\n<b>Категории</b>: {", ".join(categories)}"""
            if page_count := book.get("pageCount"):
                book_str += f"""\n<b>Число страниц</b>: {page_count}"""
            if isbn := book.get("isbn"):
                book_str += f"""\n<b>ISBN</b>: {isbn}"""

            keyboard = InlineKeyboard()
            keyboard.row(
                InlineButton("Добавить заметку", "add_note"),
                InlineButton("Возврат к результатам", "back_results"),
            )

            if hasattr(book, "longDescription"):
                keyboard.row.add(InlineButton("Показать больше информации", callback_data="more"))

            await callback_query.message.edit(book_str, reply_markup=keyboard)

        case "pagination_keyboard":
            INDEX = int(callback_query.data.split(":")[-1]) - 1
            CURRENT_BOOK = FOUND[INDEX]
            keyboard = InlineKeyboard()
            keyboard.paginate(len(FOUND), INDEX + 1, "pagination_keyboard:{number}")
            keyboard.row(
                InlineButton("Детальная информация о книге", "pagination_detail"),
                InlineButton("Добавить заметку", "add_note"),
            )
            await callback_query.message.edit(
                f"{FOUND[int(callback_query.data.split(':')[1]) - 1].get('title')}",
                reply_markup=keyboard,
            )

        case "add_note":
            await callback_query.message.edit(
                f"Введите заметку, чтобы добавить её для книги `{CURRENT_BOOK.get('title')}`"
            )
            STATE = State.ADD_NOTE

        case "back_results":
            keyboard = InlineKeyboard()
            keyboard.paginate(len(FOUND), INDEX + 1, "pagination_keyboard:{number}")
            keyboard.row(
                InlineButton("Детальная информация о книге", "pagination_detail"),
                InlineButton("Добавить заметку", "add_note"),
            )
            await callback_query.message.edit(
                f"{FOUND[INDEX].get('title')}",
                reply_markup=keyboard,
            )

        case _:
            await callback_query.message.reply("Что-то пошло не так. Попробуйте заново")


def search_menu() -> InlineKeyboardMarkup:
    button = [
        [InlineKeyboardButton("По названию", callback_data="search_title")],
        [InlineKeyboardButton("По автору", callback_data="search_author")],
        [InlineKeyboardButton("По описанию", callback_data="search_description")],
        [InlineKeyboardButton("По заметкам", callback_data="search_notes")],
    ]
    return InlineKeyboardMarkup(button)


app.run()