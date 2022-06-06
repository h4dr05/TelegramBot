import pymongo
import pprint


class BooksDatabase(pymongo.MongoClient):
    """
    Wrapper for pymongo.
    """

    URI = "mongodb://localhost:27017"

    def __init__(self, credential_path=".credentials"):
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
        super().__init__(BooksDatabase.URI)

        self.archives_db = self["Archive"]
        self.books_collection = self.archives_db["NewBooks"]

    #
    def find_book_by_title(self, query):
        query_result = self.books_collection.find({"title": {"$regex": query, "$options": "-ig"}})
        return list(query_result)

    def find_book_by_author(self, query):
        query_result = self.books_collection.find({"authors": {"$regex": query, "$options": "-i"}})
        return list(query_result)

    def find_book_by_description(self, query):
        query_result = self.books_collection.find({"longDescription": {"$regex": query, "$options": "-i"}})
        return list(query_result)


def run_db():
    database = BooksDatabase()
    pprint.pprint(database.find_book_by_author("Bruno Lowagie"))


