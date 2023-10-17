from sqlalchemy import create_engine, text


class DatabaseHandler:
    """
    Esta classe fornece métodos para conectar a um banco de dados PostgreSQL usando SQLAlchemy e executar consultas.
    """

    def __init__(self):
        # Crie a URL de conexão no construtor
        db_url = f"postgresql://postgres:postgres@localhost:5432/airbnb"
        self.engine = create_engine(db_url)

    def connect(self):
        """
        Abre uma conexão com o banco de dados.
        """
        self.connection = self.engine.connect()

    def disconnect(self):
        """
        Fecha a conexão com o banco de dados.
        """
        self.connection.close()

    def execute_query(self, query_string) -> list:
        """
        Executa uma consulta SQL e retorna os resultados.

        Args:
            query_string (str): A consulta SQL a ser executada.

        Returns:
            list: Uma lista de resultados da consulta | None.
        """
        try:
            query = text(query_string)
            result = self.connection.execute(query)
            return result.fetchall()
        except Exception as error:
            print(error)
            return None
