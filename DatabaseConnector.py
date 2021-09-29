import sqlite3
import os
from datetime import date, datetime


class DatabaseConnector():

    tables = ['LinkedIn', 'Indeed', 'Monster', 'Stepstone']
    tables_temp = ['Nouns', 'Verbs', 'Propn', 'Nums', 'Counter']

    def insert_in_table(self, table_name: str, url: str, job_description: str, city: str, radius: str, content: str) -> str:
        if os.path.exists('database.db') is False:
            self.__create_database()

        if self.__already_crawled(table_name, url, content):
            return 'Jobanzeige bereits in Datenbank'

        if content == 'Error': 
            return 'Fehler beim crawlen der Anzeige'

        date = datetime.date(datetime.now()) 
        try:
            conn = sqlite3.connect('database.db', isolation_level=None)
            cursor = conn.cursor()
            sql = 'INSERT INTO ' + table_name + \
                '(jobID, url, job, city, radius, content, date) VALUES (?, ?, ?, ?, ?, ?, ?)'
            cursor.execute(sql, (str(self.__get_maxid(table_name)+1),
                                str(url), str(job_description), str(city), str(radius), str(content), str(date)))
            conn.commit
            conn.close
            return 'Jobanzeige erfolreich gespeichert'
        except sqlite3.OperationalError as e:
            return e

    def get_all_data(self, table_name) -> sqlite3.Row:
        if os.path.exists('database.db') is False:
            self.__create_database()

        con = sqlite3.connect("database.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("select * FROM " + table_name)

        rows = cur.fetchall()
        return rows

    def get_filtered_data(self, table_name: str, job: str, city: str, radius: str, start_date: date, end_date: date) -> sqlite3.Row:
        if os.path.exists('database.db') is False:
            self.__create_database()
        con = sqlite3.connect("database.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        sql = "SELECT content FROM " + table_name + " WHERE job = '" + job + "'"

        if city != "":
            sql = sql + " AND city = '" + city + "'"
        if radius != "":
            sql = sql + " AND radius = '" + radius + "'"
        if start_date != date(2000, 1, 1):
            sql = sql + " AND date BETWEEN '" + str(start_date) + "' AND '" + str(end_date) + "'"
        cur.execute(sql) 
        rows = cur.fetchall() 
        return rows 

    def __create_table(self, table_name) -> bool:
        try:
            conn = sqlite3.connect('database.db', isolation_level=None)
            conn.execute('CREATE TABLE ' + table_name +
                         ' (jobID INTEGER, url TEXT, job TEXT, city TEXT, radius TEXT, content TEXT, date TEXT)')
            conn.commit
            conn.close
            return True
        except sqlite3.OperationalError:
            return False

    def __get_maxid(self, table_name) -> int:
        try:
            conn = sqlite3.connect('database.db', isolation_level=None)
            cursor = conn.cursor()
            sql = 'SELECT MAX(jobID) FROM ' + table_name
            cursor.execute(sql)
            max_value = 0
            temp = cursor.fetchone()[0]
            if temp is not None:
                max_value = temp
            conn.close
            return max_value
        except sqlite3.Error:
            return 0

    def __create_database(self):
        for table in self.tables:
            self.__create_table(table)

    def __already_crawled(self, tableName: str, url: str, content: str) -> bool:
        try:
            conn = sqlite3.connect('database.db', isolation_level=None)
            cursor = conn.cursor()
            sql = 'SELECT jobID FROM ' + tableName + ' WHERE url = ? OR content = ?'
            cursor.execute(sql, (url, content))
            ret_value = False
            if cursor.fetchone() is not None:
                ret_value = True
            conn.close
            return ret_value
        except sqlite3.Error:
            return False

    def __create_temp_table(self, table_name):
        try:
            conn = sqlite3.connect('database_temp.db', isolation_level=None)
            conn.execute('CREATE TABLE ' + table_name +
                         '(content TEXT)')
            conn.commit
            conn.close
            return True
        except sqlite3.OperationalError:
            return False
    
    def __create_temp_database(self):
        for table in self.tables_temp:
            self.__create_temp_table(table)
    
    def delete_temp_data(self):
        for table in self.tables_temp:
            if not self.__delete_elements(table):
                return False
        return True
    
    def __delete_elements(self, table_name: str):
        if os.path.exists('database_temp.db') is False:
            self.__create_temp_database()
        try:
            con = sqlite3.connect("database_temp.db")
            cur = con.cursor()
            cur.execute('DELETE FROM ' + table_name + ';')
            con.commit()
            con.close()
            return True
        except sqlite3.OperationalError:
            return False

    def get_all_temp_data(self, table_name) -> sqlite3.Row:
        if os.path.exists('database_temp.db') is False:
            self.__create_database()

        con = sqlite3.connect("database_temp.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM " + table_name)

        rows = cur.fetchall()
        return rows

    def insert_in_temp_table(self, table_name: str, input: list):
        if os.path.exists('database_temp.db') is False:
            self.__create_temp_database()
        if type(input) == int:
            try:
                conn = sqlite3.connect('database_temp.db', isolation_level=None)
                cursor = conn.cursor()
                sql = 'INSERT INTO ' + table_name + '(content) VALUES (?)'
                cursor.execute(sql, (str(input),))
                conn.commit
                conn.close
                return
            except sqlite3.OperationalError as e:
                return e
        for content in input:
            try:
                conn = sqlite3.connect('database_temp.db', isolation_level=None)
                cursor = conn.cursor()
                sql = 'INSERT INTO ' + table_name + '(content) VALUES (?)'
                cursor.execute(sql, (str(content),))
                conn.commit
                conn.close
            except sqlite3.OperationalError as e:
                return e
