import sqlite3 as sq3

con = sq3.connect('vales_db.db')
cur = con.cursor()
query = '''DELETE FROM vales WHERE _id > 6815'''
query1 = '''SELECT * FROM valesnombres'''
#query2 = '''UPDATE vales SET nombre = 'Policia', monto=2000 WHERE _id =6'''


# lista2=[(12,'Olivera Victor')]
# cur.executemany('INSERT INTO valesnombres VALUES (?,?)',lista2)

cur.execute(query)

con.commit()
for registro in cur.execute(query1):
    print(registro)


con.commit()
con.close()