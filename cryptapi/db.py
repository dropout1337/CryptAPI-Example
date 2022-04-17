import sqlite3, os

class Database():

    def __init__(self):
        if not os.path.exists("database.db"):
            self.new = True
        else:
            self.new = False

        self.db, self.cursor = self.connect()
        self.cursor.execute("PRAGMA journal_mode = WAL")
        self.cursor.execute("PRAGMA synchronous = OFF")
        self.cursor.execute("PRAGMA cache_size = -40960")

        self.tables = {
            "transactions": {
                "user": {
                    "type": "text"
                },
                "uuid": {
                    "type": "text"
                },
                "address_in": {
                    "type": "text"
                },
                "txid_in": {
                    "type": "text"
                },
                "confirmations": {
                    "type": "int"
                },
                "value_coin": {
                    "type": "text"
                },
                "coin": {
                    "type": "text"
                },
                "status": {
                    "type": "text"
                },
                "txid_out": {
                    "type": "text"
                },
                "value_forwarded_coin": {
                    "type": "text"
                }
            },
        }

        if self.new: self.reset()

    def close(self):
        self.db.commit()
        self.db.close()

    def connect(self):        
        db = sqlite3.connect("database.db")
        cursor = db.cursor()
        return db, cursor

    def query(self, query: str, args: tuple = None, commit: bool = True):
        output = self.cursor.execute(query) if args == None else self.cursor.execute(query, args)
        if commit: self.db.commit()
        return output
    
    def reset(self):
        for name in self.tables.keys():
            command = "CREATE TABLE %s (" % (name)
            data = self.tables[name]
            keys = list(data.keys())
            self.query("DROP TABLE IF EXISTS %s" % (name))
            
            for index in keys:
                command += "%s %s, " % (index, data[index]["type"])

            command = "%s)" % (command[:-2])
            self.query(command)