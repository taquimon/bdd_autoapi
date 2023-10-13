import mysql.connector


class MYSQLConnector:

    def __int__(self):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="",
            password="",
            database=""
        )
        print(self.mydb)


if __name__ == '__main__':
    db = MYSQLConnector()

