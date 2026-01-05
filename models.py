from sqlalchemy import Column, Integer, String, ForeignKey, Float, CHAR, Enum, SmallInteger, Numeric
from sqlalchemy.orm import relationship
from database import Base

class Country(Base):
    __tablename__ = 'country'

    Code = Column(CHAR(3), primary_key=True, index=True)  # El usuario asigna este código (ej: 'XYZ')
    Name = Column(String(52), nullable=False)
    Continent = Column(String(50), nullable=False)  # Tratado como string para simplicidad
    Region = Column(String(26), nullable=False)
    SurfaceArea = Column(Float(10, 2), default=0.00)
    IndepYear = Column(SmallInteger, nullable=True)
    Population = Column(Integer, default=0)
    LifeExpectancy = Column(Float(3, 1), nullable=True)
    GNP = Column(Float(10, 2), nullable=True)
    GNPOld = Column(Float(10, 2), nullable=True)
    LocalName = Column(String(45), default="")
    GovernmentForm = Column(String(45), default="")
    HeadOfState = Column(String(60), nullable=True)
    Capital = Column(Integer, nullable=True)
    Code2 = Column(CHAR(2), default="")

    cities = relationship("City", back_populates="country", cascade="all, delete-orphan")
    languages = relationship("CountryLanguage", back_populates="country", cascade="all, delete-orphan")


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
    Percentage = Column(Float(4,1), default=0.0)

    country = relationship('Country', back_populates='languages')