from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, or_
from typing import List
import models, schemas
from database import engine, get_db

# Inicializar BBDD
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="World DB Full API", version="3.0.0")


# ==========================================
# 1. CRUD CITY (ID Autoincremental)
# ==========================================

@app.post("/cities/", response_model=schemas.CityResponse, tags=["City"])
def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    # Validar que el país exista
    if not db.query(models.Country).filter(models.Country.Code == city.CountryCode).first():
        raise HTTPException(status_code=404, detail="El código de país no existe")

    new_city = models.City(**city.dict())
    db.add(new_city)
    db.commit()
    db.refresh(new_city)
    return new_city


@app.get("/cities/", response_model=List[schemas.CityResponse], tags=["City"])
def list_cities(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return db.query(models.City).offset(skip).limit(limit).all()


@app.get("/cities/{id}", response_model=schemas.CityResponse, tags=["City"])
def get_city(id: int, db: Session = Depends(get_db)):
    city = db.query(models.City).filter(models.City.ID == id).first()
    if not city: raise HTTPException(status_code=404, detail="Ciudad no encontrada")
    return city


@app.put("/cities/{id}", response_model=schemas.CityResponse, tags=["City"])
def update_city(id: int, city_data: schemas.CityUpdate, db: Session = Depends(get_db)):
    city = db.query(models.City).filter(models.City.ID == id).first()
    if not city: raise HTTPException(status_code=404, detail="Ciudad no encontrada")

    for key, value in city_data.dict(exclude_unset=True).items():
        setattr(city, key, value)
    db.commit()
    db.refresh(city)
    return city


@app.delete("/cities/{id}", tags=["City"])
def delete_city(id: int, db: Session = Depends(get_db)):
    city = db.query(models.City).filter(models.City.ID == id).first()
    if not city: raise HTTPException(status_code=404, detail="Ciudad no encontrada")
    db.delete(city)
    db.commit()
    return {"message": "Ciudad eliminada"}


# ==========================================
# 2. CRUD COUNTRY (ID manual de 3 letras)
# ==========================================

@app.post("/countries/", response_model=schemas.CountryResponse, tags=["Country"])
def create_country(country: schemas.CountryCreate, db: Session = Depends(get_db)):
    if db.query(models.Country).filter(models.Country.Code == country.Code).first():
        raise HTTPException(status_code=400, detail="El código de país ya existe")

    new_country = models.Country(**country.dict())
    db.add(new_country)
    db.commit()
    db.refresh(new_country)
    return new_country


@app.get("/countries/", response_model=List[schemas.CountryResponse], tags=["Country"])
def list_countries(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return db.query(models.Country).offset(skip).limit(limit).all()


@app.get("/countries/{code}", response_model=schemas.CountryResponse, tags=["Country"])
def get_country(code: str, db: Session = Depends(get_db)):
    country = db.query(models.Country).filter(models.Country.Code == code.upper()).first()
    if not country: raise HTTPException(status_code=404, detail="País no encontrado")
    return country


@app.put("/countries/{code}", response_model=schemas.CountryResponse, tags=["Country"])
def update_country(code: str, data: schemas.CountryUpdate, db: Session = Depends(get_db)):
    country = db.query(models.Country).filter(models.Country.Code == code.upper()).first()
    if not country: raise HTTPException(status_code=404, detail="País no encontrado")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(country, key, value)
    db.commit()
    db.refresh(country)
    return country


@app.delete("/countries/{code}", tags=["Country"])
def delete_country(code: str, db: Session = Depends(get_db)):
    country = db.query(models.Country).filter(models.Country.Code == code.upper()).first()
    if not country: raise HTTPException(status_code=404, detail="País no encontrado")
    # Nota: SQLAlchemy cascade borrará ciudades e idiomas asociados automáticamente si está configurado en models.py
    db.delete(country)
    db.commit()
    return {"message": f"País {code} eliminado junto con sus ciudades e idiomas."}


# ==========================================
# 3. CRUD COUNTRYLANGUAGE (Clave Compuesta)
# ==========================================

@app.post("/languages/", response_model=schemas.LanguageResponse, tags=["Language"])
def create_language(lang: schemas.LanguageCreate, db: Session = Depends(get_db)):
    # Verificar existencia (Clave compuesta)
    exists = db.query(models.CountryLanguage).filter(
        models.CountryLanguage.CountryCode == lang.CountryCode,
        models.CountryLanguage.Language == lang.Language
    ).first()
    if exists:
        raise HTTPException(status_code=400, detail="Este idioma ya existe para este país")

    new_lang = models.CountryLanguage(**lang.dict())
    db.add(new_lang)
    db.commit()
    db.refresh(new_lang)
    return new_lang


@app.get("/languages/", response_model=List[schemas.LanguageResponse], tags=["Language"])
def list_languages(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return db.query(models.CountryLanguage).offset(skip).limit(limit).all()


# Endpoint para obtener un idioma específico: Requiere AMBOS IDs
@app.get("/languages/{country_code}/{language}", response_model=schemas.LanguageResponse, tags=["Language"])
def get_language(country_code: str, language: str, db: Session = Depends(get_db)):
    lang = db.query(models.CountryLanguage).filter(
        models.CountryLanguage.CountryCode == country_code.upper(),
        models.CountryLanguage.Language == language
    ).first()
    if not lang: raise HTTPException(status_code=404, detail="Registro de idioma no encontrado")
    return lang


@app.put("/languages/{country_code}/{language}", response_model=schemas.LanguageResponse, tags=["Language"])
def update_language(country_code: str, language: str, data: schemas.LanguageUpdate, db: Session = Depends(get_db)):
    lang = db.query(models.CountryLanguage).filter(
        models.CountryLanguage.CountryCode == country_code.upper(),
        models.CountryLanguage.Language == language
    ).first()
    if not lang: raise HTTPException(status_code=404, detail="Registro de idioma no encontrado")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(lang, key, value)
    db.commit()
    db.refresh(lang)
    return lang


@app.delete("/languages/{country_code}/{language}", tags=["Language"])
def delete_language(country_code: str, language: str, db: Session = Depends(get_db)):
    lang = db.query(models.CountryLanguage).filter(
        models.CountryLanguage.CountryCode == country_code.upper(),
        models.CountryLanguage.Language == language
    ).first()
    if not lang: raise HTTPException(status_code=404, detail="Registro de idioma no encontrado")

    db.delete(lang)
    db.commit()
    return {"message": "Idioma eliminado"}