import pymongo
import pprint
from enum import Enum


class BooksDatabase(pymongo.MongoClient):
    """
    Wrapper for pymongo.
    """

    URI = "mongodb://localhost:27017"

    class SearchMode(Enum):
        TITLE = 1
        AUTHOR = 2
        DESCRIPTION = 3
    TITLE = SearchMode.TITLE
    AUTHOR = SearchMode.AUTHOR
    DESCRIPTION = SearchMode.DESCRIPTION

    def __init__(self, credential_path=".credentials") -> None:
        """
        Initialize the database connection.
        """
        with open(credential_path) as cred_fd:
            """
            dbusername=
            dbpassword=
            authdb=
            """
            credentials = cred_fd.read().strip().split("\n")
            try:
                username = credentials[0].split("=")[1]
                password = credentials[1].split("=")[1]
                authdb = credentials[2].split("=")[1]
            except IndexError:
                raise Exception(
                    f"Invalid credentials file format, please double check that it is filled out and the correct path was passed in (given: {credential_path}).")

        super().__init__(BooksDatabase.URI, username=username,
                         password=password, authSource=authdb)

        self.archives_db = self["Archive"]
        self.books_collection = self.archives_db["NewBooks"]

    ### Search Method ###
    def find_book(self, query, mode: SearchMode) -> pymongo.cursor.Cursor:
        # query = "\\b" + query + "\\b"
        match mode:
            case self.TITLE:
                return self.books_collection.find(
                    {"title": {"$regex": "\\b"+query+"\\b\\s", "$options": "-i"}})
            case self.AUTHOR:
                return self.books_collection.find(
                    {"authors": {"$regex": "\\b"+query+"\\b\\s", "$options": "-i"}})
            case self.DESCRIPTION:
                return self.books_collection.find({"longDescription": {"$regex": "\\b"+query+"\\b\\s", "$options": "-i"}, 
                                                "shortDescription": {"$regex": "\\b"+query+"\\b\\s", "$options": "-i"}})
            case _:
                raise Exception(f"Invalid search mode: {mode}")
