import pymongo


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

        self.archives_db = self["Archives"]
        self.books_collection = self.archives_db["Books"]
