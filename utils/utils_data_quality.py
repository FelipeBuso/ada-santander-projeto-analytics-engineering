db = DatabaseHandler()
data = db.execute_query('SELECT * FROM raw.listings')
print(data)