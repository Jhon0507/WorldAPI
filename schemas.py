from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List

# CITY
class CityBase(BaseModel):
    Name: str
    CountryCode: str = Field(..., max_length=3)
    District: str
    Population: int

class CityCreate(CityBase):
    pass

class CityUpdate(BaseModel):
    Name: Optional[str] = None
    District: Optional[str] = None
    Population: Optional[int] = None

class CityResponse(CityBase):
    ID: int
    model_config = ConfigDict(from_attributes=True)

# LANGUAGE
class LanguageBase(BaseModel):
    CountryCode: str = Field(..., max_length=3)
    Language: str
    IsOfficial: str = Field(..., pattern="^(T|F)$") # Solo permite 'T' o 'F'
    Percentage: float

class LanguageCreate(LanguageBase):
    pass

class LanguageUpdate(BaseModel):
    # No permitimos cambiar CountryCode ni Language porque son Primary Key
    IsOfficial: Optional[str] = Field(None, pattern="^(T|F)$")
    Percentage: Optional[float] = None

class LanguageResponse(LanguageBase):
    model_config = ConfigDict(from_attributes=True)

# COUNTRY
class CountryBase(BaseModel):
    Code: str = Field(..., max_length=3)
    Name: str
    Continent: str
    Region: str
    SurfaceArea: float
    Population: int
    LocalName: str
    GovernmentForm: str
    Code2: str = Field(..., max_length=2)

class CountryCreate(CountryBase):
    IndepYear: Optional[int] = None
    LifeExpectancy: Optional[float] = None
    GNP: Optional[float] = None
    HeadOfState: Optional[str] = None

class CountryUpdate(BaseModel):
    Name: Optional[str] = None
    Population: Optional[int] = None
    HeadOfState: Optional[str] = None
    GNP: Optional[float] = None
    LifeExpectancy: Optional[float] = None

class CountryResponse(CountryBase):
    HeadOfState: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)