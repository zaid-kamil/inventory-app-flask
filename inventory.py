import sqlite3 

class Database:
    # contructor 
    def __init__(self, file = 'db.sqlite3'):
        self.con = sqlite3.connect(file)
        self.create_table() # created when used
        self.create_full_text_search() # search system

    # query execution
    def run(self,query):
        try:
            self.con.execute(query.lower())
            self.con.commit() # save database lik ctrl + s
            return True
        except Exception as e:
            if 'create' not in query.lower():
                print(query)
                print('error',e)
            return False

    # create table for inventoryloyee
    def create_table(self):
        query = """
        CREATE TABLE inventory ( id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        qty INTEGER,
        price DOUBLE)
        """
        return self.run(query)

    def create_full_text_search(self):
        query= """
        CREATE VIRTUAL TABLE finder USING fts5(name, qty, price);
        """
        return self.run(query)


    # add inventoryloyee
    def add(self, name,qty=1,price=0.0):
        query=f"""
        INSERT INTO inventory VALUES(null, '{name}',{qty},{price})
        """
        return self.run(query)

    # view all data
    def viewAll(self):
        query= "SELECT * FROM inventory ORDER BY qty "
        data = self.con.execute(query)
        return data.fetchall()

    # edit
    def edit(self,id, name,qty=1,price=0.0):
        query=f"""
        UPDATE inventory SET name ='{name}', qty={qty} ,price={price} WHERE id = {id} 
        """
        return self.run(query)
    # delete
    def delete(self,id):
        query=f"""
        DELETE FROM inventory WHERE id ={id}
        """
        return self.run(query)


    def viewById(self,id):
        query= f"SELECT * FROM inventory WHERE id={id}"
        data = self.con.execute(query)
        return data.fetchone()
        

    def search(self,value=None):
        if not value.isnumeric():
            query=f"""
            SELECT * FROM inventory WHERE name LIKE '%{value}%';
            """
            print(query)
            data = self.con.execute(query)
            return data.fetchall()
        elif value.isnumeric():
            query=f"""
            SELECT * FROM inventory WHERE qty={value};
            """
            print(query)
            data = self.con.execute(query)
            return data.fetchall()
        else:
            return  None
