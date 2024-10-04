
import pymysql

conn = pymysql.connect(
    host="localhost",
    user="alfred",
    password="Ka075.",
    database="autoflaskapi",
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

cursor = conn.cursor()
sql_query = """CREATE TABLE autos (
    id_auto INTEGER PRIMARY KEY AUTO_INCREMENT,
    id_parking INTEGER NOT NULL,
    matricule TEXT NOT NULL
)"""

cursor.execute(sql_query)
conn.close()
print("datavel and table is created successfully")
