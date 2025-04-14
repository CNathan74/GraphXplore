from sqlalchemy import (
    create_engine, Column, Integer, String, ForeignKey, BigInteger, DateTime, Table
)
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
import os

# Chemin de la base SQLite locale
DB_FILENAME = "grandeurs.db"

# Vérifie si la base existe
db_exists = os.path.exists(DB_FILENAME)

# Création de l'engine
engine = create_engine(f"sqlite:///{DB_FILENAME}", echo=True)
Base = declarative_base()

# Tables associatives
Onglet_Grandeur = Table(
    "Onglet_Grandeur", Base.metadata,
    Column("id_onglet", Integer, ForeignKey("Onglet.id"), primary_key=True),
    Column("id_grandeur", Integer, ForeignKey("Grandeur.id"), primary_key=True)
)

# Définition des classes
class Onglet(Base):
    __tablename__ = "Onglet"
    id = Column(Integer, primary_key=True)
    nom = Column(String(100))
    grandeurs = relationship("Grandeur", secondary=Onglet_Grandeur, back_populates="onglets")


class File(Base):
    __tablename__ = "File"
    id = Column(Integer, primary_key=True)
    nom = Column(String(255))
    path = Column(String(255))
    last_modif = Column(DateTime)
    grandeurs = relationship("Grandeur", back_populates="file")


class Type_Grandeur(Base):
    __tablename__ = "Type_Grandeur"
    nom = Column(String(100), primary_key=True)
    grandeurs = relationship("Grandeur", back_populates="type_grandeur")


class Grandeur(Base):
    __tablename__ = "Grandeur"
    id = Column(Integer, primary_key=True)
    nom_typeGrandeur = Column(String(100), ForeignKey("Type_Grandeur.nom"))
    id_file = Column(Integer, ForeignKey("File.id"))
    
    deemebeding = Column(String(100))
    facePort = Column(String(100))
    frequence = Column(BigInteger)
    lineLength = Column(Integer)
    lot = Column(Integer)
    parametre = Column(String(100))
    portWidth = Column(Integer)
    data = Column(String(100))

    file = relationship("File", back_populates="grandeurs")
    type_grandeur = relationship("Type_Grandeur", back_populates="grandeurs")
    onglets = relationship("Onglet", secondary=Onglet_Grandeur, back_populates="grandeurs")

def create_database():
    # Création de la base si elle n'existe pas
    if not db_exists:
        Base.metadata.create_all(engine)
        print("Base de données créée.")
    else:
        print("Base de données trouvée.")