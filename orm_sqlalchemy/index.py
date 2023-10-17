from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import Session
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class Listining(Base):
    __tablename__ = "listining"

    id: Mapped[int] = mapped_column(primary_key=True)
    listining_id: Mapped[int]
    listing_url: Mapped[str]
    scrape_id: Mapped[int]
    host_id: Mapped[int]
    host_listings_count: Mapped[int]
    reviews: Mapped[List["Reviews"]] = relationship(
        back_populates="listining", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"listining(id={self.id!r}, listining_id={self.listining_id!r}, listing_url={self.listing_url!r})"


class Reviews(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(primary_key=True)
    listing_id: Mapped[int] = mapped_column(ForeignKey("listining.listining_id"))
    review_id: Mapped[int]
    date: Mapped[str]
    reviewer_id: Mapped[int]
    reviewer_name: Mapped[str]
    comments: Mapped[Optional[str]]

    listining: Mapped["Listining"] = relationship(back_populates="reviews")

    def __repr__(self) -> str:
        return (
            f"Reviews(id={self.id!r}, review_id={self.review_id!r}, date={self.date!r})"
        )


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

    def create_tables(self):
        """
        Cria as tabelas no banco de dados com base classes dos recursos
        """
        Base.metadata.create_all(self.engine)

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

    def post_listining(self, data: List[dict]):
        """
        Grava os dados na tabela Lisiting.

        Args:
            data (list[dict]): Lista de dicionários com os dados.

        """
        with Session(self.engine) as session:
            list_listining = list()
            for payload in data:
                list_listining.append(Listining(**payload))
            try:
                session.add_all(list_listining)
                session.commit()
            except Exception as error:
                print(error)

    def post_reviews(self, data: List[dict]):
        """
        Grava os dados na tabela Reviews.

        Args:
            data (list[dict]): Lista de dicionários com os dados.

        """
        with Session(self.engine) as session:
            list_reviews = list()
            for payload in data:
                list_reviews.append(Reviews(**payload))
            try:
                session.add_all(list_reviews)
                session.commit()
            except Exception as error:
                print(error)
