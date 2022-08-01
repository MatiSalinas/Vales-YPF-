import sqlite3 as sq3

con = sq3.connect('vales_db.db')
cur = con.cursor()

instruct1 = '''CREATE TABLE IF NOT EXISTS vales (
  _id INTEGER PRIMARY KEY AUTOINCREMENT,  
  nombre varchar(45) DEFAULT NULL,
  monto FLOAT  DEFAULT NULL,
  estado BIT DEFAULT 0)'''

instruct2 = '''CREATE TABLE IF NOT EXISTS valesnombres (
  _id INTEGER PRIMARY KEY AUTOINCREMENT,  
  nombre varchar(45) DEFAULT NULL)'''

cur.execute(instruct1)

lista1 = [(1,'Policia',1000.0,0),(2,'Dir. Gral. Admin.',1000.0,0),(3,'Municipalidad.',1000.0,0),(4,'Leito.',1000.0,0),(5,'Mati.',1000.0,0),(6,'Mati.',1000.0,0)]

cur.executemany('INSERT INTO vales VALUES (?,?,?,?)',lista1)

cur.execute(instruct2)

lista2=[(0,'Policia'),(1,'Dir. Gral. Admin'),(2,'Leito'),(3,'Municipalidad'),(4,'Empleados')]

cur.executemany('INSERT INTO valesnombres VALUES (?,?)',lista2)

query1 = '''SELECT * FROM vales'''

query2 = '''SELECT * FROM valesnombres'''



for registro in cur.execute(query1):
    print(registro)

for registro in cur.execute(query2):
    print(registro)

con.commit()
con.close()