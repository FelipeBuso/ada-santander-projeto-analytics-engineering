from sqlalchemy import create_engine, text


class DatabaseHandler:
    def __init__(self):
        # Crie a URL de conexão no construtor
        db_url = f"postgresql://postgres:postgres@localhost:5432/airbnb"
        self.engine = create_engine(db_url)

    def connect(self):
        # Abra uma conexão com o banco de dados
        self.connection = self.engine.connect()

    def disconnect(self):
        # Feche a conexão com o banco de dados
        self.connection.close()

    def execute_query(self, query_string):
        # Execute uma consulta SQL e retorne os resultados
        query = text(query_string)
        result = self.connection.execute(query)
        return result.fetchall()
