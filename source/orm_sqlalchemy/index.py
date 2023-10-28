import os
from datetime import date
import pandas as pd
from typing import List
from typing import Optional
from sqlalchemy import BigInteger
from sqlalchemy import create_engine
from sqlalchemy import CursorResult
from sqlalchemy import ForeignKey
from sqlalchemy import text
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Session
from sqlalchemy.orm import relationship
from sqlalchemy.exc import IntegrityError
from dotenv import load_dotenv


class Base(DeclarativeBase):
    pass


class Listings(Base):
    __tablename__ = "listings"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    listing_url: Mapped[str]
    scrape_id: Mapped[int] = mapped_column(BigInteger)
    last_scraped: Mapped[date]
    source: Mapped[str]
    name: Mapped[str]
    description: Mapped[Optional[str]]
    neighborhood_overview: Mapped[Optional[str]]
    picture_url: Mapped[str]
    host_id: Mapped[int]
    host_url: Mapped[str]
    host_name: Mapped[Optional[str]]
    host_since: Mapped[Optional[str]]
    host_location: Mapped[Optional[str]]
    host_about: Mapped[Optional[str]]
    host_response_time: Mapped[Optional[str]]
    host_response_rate: Mapped[Optional[float]]
    host_acceptance_rate: Mapped[Optional[str]]
    host_is_superhost: Mapped[bool]
    host_thumbnail_url: Mapped[Optional[str]]
    host_picture_url: Mapped[Optional[str]]
    host_neighbourhood: Mapped[Optional[str]]
    host_listings_count: Mapped[float]
    host_total_listings_count: Mapped[float]
    host_verifications: Mapped[Optional[str]]
    host_has_profile_pic: Mapped[bool]
    host_identity_verified: Mapped[bool]
    # neighbourhood: Mapped[Optional[str]] # removida (usar neighbourhood_cleansed)
    neighbourhood_cleansed: Mapped[str]
    # neighbourhood_group_cleansed: Mapped[float] # removida
    latitude: Mapped[float]
    longitude: Mapped[float]
    property_type: Mapped[str]
    room_type: Mapped[str]
    accommodates: Mapped[int]
    # bathrooms: Mapped[float] # removida
    bathrooms_text: Mapped[Optional[str]]
    bedrooms: Mapped[float]
    beds: Mapped[int]
    amenities: Mapped[str]
    price: Mapped[str]
    minimum_nights: Mapped[int]
    maximum_nights: Mapped[int]
    minimum_minimum_nights: Mapped[int]
    maximum_minimum_nights: Mapped[int]
    minimum_maximum_nights: Mapped[int]
    maximum_maximum_nights: Mapped[int]
    minimum_nights_avg_ntm: Mapped[float]
    maximum_nights_avg_ntm: Mapped[float]
    # calendar_updated: Mapped[float] # removida
    has_availability: Mapped[bool]
    availability_30: Mapped[int]
    availability_60: Mapped[int]
    availability_90: Mapped[int]
    availability_365: Mapped[int]
    calendar_last_scraped: Mapped[date]
    number_of_reviews: Mapped[int]
    number_of_reviews_ltm: Mapped[int]
    number_of_reviews_l30d: Mapped[int]
    first_review: Mapped[Optional[date]]
    last_review: Mapped[Optional[date]]
    review_scores_rating: Mapped[Optional[float]]
    review_scores_accuracy: Mapped[Optional[float]]
    review_scores_cleanliness: Mapped[Optional[float]]
    review_scores_checkin: Mapped[Optional[float]]
    review_scores_communication: Mapped[Optional[float]]
    review_scores_location: Mapped[Optional[float]]
    review_scores_value: Mapped[Optional[float]]
    # license: Mapped[float] # removida
    instant_bookable: Mapped[bool]
    calculated_host_listings_count: Mapped[int]
    calculated_host_listings_count_entire_homes: Mapped[int]
    calculated_host_listings_count_private_rooms: Mapped[int]
    calculated_host_listings_count_shared_rooms: Mapped[int]
    reviews_per_month: Mapped[Optional[float]]

    reviews: Mapped[List["Reviews"]] = relationship(
        back_populates="listining", cascade="all, delete-orphan"
    )
    calendars: Mapped[List["Calendars"]] = relationship(
        back_populates="listining", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"listining(id={self.id!r}, listining_id={self.listining_id!r}, listing_url={self.listing_url!r})"


class Reviews(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    listing_id: Mapped[int] = mapped_column(ForeignKey("listings.id"))
    date: Mapped[str]
    reviewer_id: Mapped[int] = mapped_column(BigInteger)
    reviewer_name: Mapped[str]
    comments: Mapped[Optional[str]]

    listining: Mapped["Listings"] = relationship(back_populates="reviews")

    def __repr__(self) -> str:
        return (
            f"Reviews(id={self.id!r}, review_id={self.review_id!r}, date={self.date!r})"
        )


class Calendars(Base):
    __tablename__ = "calendars"

    id: Mapped[int] = mapped_column(primary_key=True)
    listing_id: Mapped[int] = mapped_column(ForeignKey("listings.id"))
    date: Mapped[str]
    available: Mapped[bool]
    price: Mapped[float]
    adjusted_price: Mapped[float]
    minimum_nights: Mapped[float]
    maximum_nights: Mapped[float]

    listining: Mapped["Listings"] = relationship(back_populates="calendars")

    def __repr__(self) -> str:
        return (
            f"Reviews(id={self.id!r}, avaiable={self.available!r}, date={self.date!r})"
        )


class DatabaseHandler:
    """
    Esta classe fornece métodos para conectar a um banco de dados PostgreSQL usando SQLAlchemy.
    """

    def __init__(self):
        load_dotenv()
        db_url = os.environ.get("POSTGRES_URI")
        self._engine = create_engine(db_url)

    tables = {"listings": Listings, "reviews": Reviews, "calendars": Calendars}

    def get_engine(self):
        return self._engine

    def connect(self):
        """
        Abre uma conexão com o banco de dados.
        """
        self.connection = self._engine.connect()
        return self.connection

    def disconnect(self):
        """
        Fecha a conexão com o banco de dados.
        """
        self.connection.close()

    def create_tables(self, schema_name: str) -> None:
        """
        Cria as tabelas no schema informado, com base nas classes dos recursos

         Args:
            schema_name (str): Nome do schema onde será criado as tabelas.

        """
        if self.connect().dialect.has_schema(self.connect(), schema_name):
            for key in self.tables.keys():
                table = self.tables[key]
                table.__table__.schema = schema_name

        Base.metadata.create_all(bind=self.get_engine())
        self.disconnect()

    def execute_query(self, query_string) -> CursorResult:
        """
        Executa uma consulta SQL e retorna os resultados.

        Args:
            query_string (str): A consulta SQL a ser executada.

        Returns:
            (CursorResult) objeto com resultado da query
        """
        try:
            query = text(query_string)
            result = self.connect().execute(query)
            return result
        except Exception as error:
            print(error)
            return None

    def post_data(self, table: str, data: List[dict], schema: str) -> None:
        """
        Grava os dados na tabela informada.

        Args:
            table (str): Nome da tabela onde será inserido os dados.
            data (list[dict]): Lista de dicionários com os dados.
            schema (str): Nome do schema onde as tabelas estão localizadas no banco de dados.
        """

        if not table in self.tables:
            raise Exception("Model não localizado")

        # Cria as tabelas caso não existam
        self.create_tables(schema)

        # Retorna a classe da tabela informada
        selected_table: DeclarativeBase = self.tables[table]

        if self.connect().dialect.has_schema(self.connect(), schema):
            with Session(self._engine) as session:
                # list_data = list()
                for payload in data:
                    # list_data.append(selected_table(**payload))
                    try:
                        session.add(selected_table(**payload))
                        session.commit()
                    except IntegrityError as error:
                        session.rollback()
                        print("Dado já existente")
                    except Exception as e:
                        session.rollback()
                        print(e)
        else:
            raise Exception("Não existe o schema no banco de dados")

    def dataframe_to_sql(self, table: str, df: pd.DataFrame, schema: str) -> None:
        """
        Grava os dados na tabela informada usando o método to_sql do Pandas.

        Args:
            table (str): Nome da tabela onde será inserido os dados.
            df (DataFrame): DataFrame com os dados.
            schema (str): Nome do schema onde as tabelas estão localizadas no banco de dados.
        """
        batch_size = 10_000
        start_idx = 0

        while start_idx < len(df):
            batch_df = df.iloc[start_idx : start_idx + batch_size]
            batch_df.to_sql(
                name=table,
                con=self.get_engine(),
                schema=schema,
                if_exists="append",
                index=False,
            )
            start_idx += batch_size
