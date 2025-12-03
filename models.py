from sqlalchemy import Column, Integer, String, ForeignKey, Float, CHAR, Enum
from sqlalchemy.orm import relationship
from database import Base

class Country(Base):
    __tablename__ = 'country'

    Code = Column(CHAR(3), primary_key=True, index=True)
    Name = Column(String(64), nullable=False)
    Continent = Column(String(64), nullable=False)
    Region = Column(String(32), nullable=False)
    Population = Column(Integer, default=0)
    HeadOfState = Column(String(64), nullable=True)

    # Relaciones
    cities = relationship('City', back_populates='country')
    languages = relationship('CountryLanguage', back_populates='country')


class City(Base):
    __tablename__ = 'city'

    ID = Column(Integer, primary_key=True, index=True, autoincrement=True)
    Name = Column(String(64), nullable=False)
    CountryCode = Column(CHAR(3), ForeignKey('country.Code'), nullable=False)
    District = Column(String(32), nullable=False)
    Population = Column(Integer, default=0)

    country = relationship('Country', back_populates='cities')


class CountryLanguage(Base):
    __tablename__ = 'countrylanguage'

    CountryCode = Column(CHAR(3), ForeignKey('country.Code'), primary_key=True)
    Language = Column(String(32), primary_key=True)
    IsOfficial = Column(Enum('T','F'), default='F')
    Percentage = Column(Float, default=0.0)

    country = relationship('Country', back_populates='languages')