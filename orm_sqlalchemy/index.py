from typing import List, Listining
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import BigInteger
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import Session
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class Listings(Base):
    __tablename__ = "listings"

    id: Mapped[int] = mapped_column(primary_key=True)
    listing_url: Mapped[str]
    scrape_id: Mapped[int] = mapped_column(BigInteger)
    last_scraped: Mapped[str]
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
    host_response_rate: Mapped[Optional[str]]
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
    neighbourhood: Mapped[Optional[str]]
    neighbourhood_cleansed: Mapped[str]
    neighbourhood_group_cleansed: Mapped[float]
    latitude: Mapped[float]
    longitude: Mapped[float]
    property_type: Mapped[str]
    room_type: Mapped[str]
    accommodates: Mapped[int]
    bathrooms: Mapped[float]
    bathrooms_text: Mapped[Optional[str]]
    bedrooms: Mapped[float]
    beds: Mapped[float]
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
    calendar_updated: Mapped[float]
    has_availability: Mapped[bool]
    availability_30: Mapped[int]
    availability_60: Mapped[int]
    availability_90: Mapped[int]
    availability_365: Mapped[int]
    calendar_last_scraped: Mapped[str]
    number_of_reviews: Mapped[int]
    number_of_reviews_ltm: Mapped[int]
    number_of_reviews_l30d: Mapped[int]
    first_review: Mapped[Optional[str]]
    last_review: Mapped[Optional[str]]
    review_scores_rating: Mapped[float]
    review_scores_accuracy: Mapped[float]
    review_scores_cleanliness: Mapped[float]
    review_scores_checkin: Mapped[float]
    review_scores_communication: Mapped[float]
    review_scores_location: Mapped[float]
    review_scores_value: Mapped[float]
    license: Mapped[float]
    instant_bookable: Mapped[bool]
    calculated_host_listings_count: Mapped[int]
    calculated_host_listings_count_entire_homes: Mapped[int]
    calculated_host_listings_count_private_rooms: Mapped[int]
    calculated_host_listings_count_shared_rooms: Mapped[int]
    reviews_per_month: Mapped[float]

    reviews: Mapped[List["Reviews"]] = relationship(
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
