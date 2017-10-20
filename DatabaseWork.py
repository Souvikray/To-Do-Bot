import sqlite3

class BotDB:
    def __init__(self,dbname="todo.sqlite"):
        # we assign the database to 'dbname' attribute
        self.dbname = dbname
        # we connect to the database and store the connection in 'con' attribute
        self.con = sqlite3.connect(dbname)

    def setup(self):
        stmt = "CREATE TABLE IF NOT EXISTS items (work text,user text)"
        # add an index to the work table to speed up the deletion operation
        workindex = "CREATE INDEX IF NOT EXISTS workIndex ON items (work ASC)"
        # add an index to the user table to speed up the retrieval of items
        userindex = "CREATE INDEX IF NOT EXISTS userIndex ON items (user ASC)"
        self.con.execute(stmt)
        self.con.execute(workindex)
        self.con.execute(userindex)
        self.con.commit()

    def add_item(self,item_text,user):
        stmt = "INSERT INTO items (work,user) VALUES (?,?)"
        # we pass the text and chat id as the argument
        args = (item_text,user)
        # we execute the SQL statement
        self.con.execute(stmt,args)
        self.con.commit()

    def delete_item(self,item_text,user):
        stmt = "DELETE FROM items WHERE work = (?) AND user = (?)"
        args = (item_text,user)
        self.con.execute(stmt,args)
        self.con.commit()

    def get_items(self,user):
        stmt = "SELECT work FROM items WHERE user = (?)"
        args = (user,)
        # return a list of all the work for the particular user
        return [x[0] for x in self.con.execute(stmt,args)]

