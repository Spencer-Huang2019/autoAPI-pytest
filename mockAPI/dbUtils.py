import MySQLdb

class database(object):
    def connect(self):
        self.conn = MySQLdb.connect(
            host="127.0.0.1",
            port=3306,
            user='test',
            passwd='test123',
            db='myfirstbd',
            charset='utf8'
        )
        return self.conn

