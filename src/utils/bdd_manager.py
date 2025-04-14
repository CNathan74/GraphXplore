from sqlalchemy import (
    create_engine, Column, Integer, String, ForeignKey, BigInteger, DateTime, Table
)
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
from datetime import datetime
import os

# Chemin de la base SQLite locale
DB_FILENAME = "grandeurs.db"

# Vérifie si la base existe
db_exists = os.path.exists(DB_FILENAME)

# Création de l'engine
engine = create_engine(f"sqlite:///{DB_FILENAME}", echo=True)
Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()

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

    file = relationship("File", back_populates="grandeurs")
    type_grandeur = relationship("Type_Grandeur", back_populates="grandeurs")
    onglets = relationship("Onglet", secondary=Onglet_Grandeur, back_populates="grandeurs")
    valeurs = relationship("Valeur_Grandeur", back_populates="grandeur")

class Valeur_Grandeur(Base):
    __tablename__ = "Valeur_Grandeur"
    id = Column(Integer, primary_key=True)
    nom = Column(String(100))          # nom de l'attribut (ex: "pression", "frequence")
    valeur = Column(String(255))       # valeur enregistrée (toujours en string pour la flexibilité)
    id_grandeur = Column(Integer, ForeignKey("Grandeur.id"))

    grandeur = relationship("Grandeur", back_populates="valeurs")


def create_database():
    # Création de la base si elle n'existe pas
    if not db_exists:
        Base.metadata.create_all(engine)
        print("Base de données créée.")
    else:
        print("Base de données trouvée.")

############################# Onglet #############################
def ajouter_onglet(nom):
    onglet = Onglet(nom=nom)
    session.add(onglet)
    session.commit()
    return onglet

def supprimer_onglet(onglet_id):
    onglet = session.query(Onglet).get(onglet_id)
    if onglet:
        session.delete(onglet)
        session.commit()

def lire_all_onglets():
    onglets = session.query(Onglet).all()
    for o in onglets:
        print(f"Onglet {o.id} : {o.nom}")
    return onglets

def lire_onglet(onglet_id):
    onglet = session.query(Onglet).get(onglet_id)
    return onglet

############################# File #############################
def ajouter_file(nom, path, last_modif=None):
    if last_modif is None:
        last_modif = datetime.now()
    fichier = File(nom=nom, path=path, last_modif=last_modif)
    session.add(fichier)
    session.commit()
    return fichier

def supprimer_file(file_id):
    fichier = session.query(File).get(file_id)
    if fichier:
        session.delete(fichier)
        session.commit()

def lire_all_files():
    fichiers = session.query(File).all()
    for f in fichiers:
        print(f"File {f.id} : {f.nom}, Path: {f.path}, Dernière modif: {f.last_modif}")
    return fichiers

############################# Type grandeur #############################
def ajouter_type_grandeur(nom):
    type_g = Type_Grandeur(nom=nom)
    session.add(type_g)
    session.commit()
    return type_g

def supprimer_type_grandeur(nom):
    type_g = session.query(Type_Grandeur).get(nom)
    if type_g:
        session.delete(type_g)
        session.commit()

def lire_all_types_grandeur():
    types = session.query(Type_Grandeur).all()
    for t in types:
        print(f"Type de Grandeur : {t.nom}")
    return types

############################# Grandeur #############################
def ajouter_grandeur(nom_typeGrandeur, id_file, **kwargs):
    grandeur = Grandeur(nom_typeGrandeur=nom_typeGrandeur, id_file=id_file, **kwargs)
    session.add(grandeur)
    session.commit()
    return grandeur

def supprimer_grandeur(grandeur_id):
    grandeur = session.query(Grandeur).get(grandeur_id)
    if grandeur:
        session.delete(grandeur)
        session.commit()

def lire_all_grandeurs():
    grandeurs = session.query(Grandeur).all()
    for g in grandeurs:
        print(f"Grandeur {g.id} | Type: {g.nom_typeGrandeur} | Fichier ID: {g.id_file} | Fréquence: {g.frequence}")
    return grandeurs

def lire_grandeur(nom_type_grandeur, num_page, nombre):
    """
    Récupère un nombre de grandeurs pour un type donné, à partir d'un index donné (pagination).
    """
    query = session.query(Grandeur).filter_by(nom_typeGrandeur=nom_type_grandeur)
    grandeurs = query.offset(num_page * nombre).limit(nombre).all()
    
    #for g in grandeurs:
    #    print(f"[{g.id}] Paramètre: {g.parametre} | Fréquence: {g.frequence} | File ID: {g.id_file}")
    
    return grandeurs

############################# Valuer Grandeur #############################
def ajouter_valeur_grandeur(id_grandeur, nom, valeur):
    v = Valeur_Grandeur(id_grandeur=id_grandeur, nom=nom, valeur=str(valeur))
    session.add(v)
    session.commit()
    print(f"✅ Valeur '{nom}' = {valeur} ajoutée à grandeur {id_grandeur}.")
    return v

def supprimer_valeur_grandeur(id_valeur):
    v = session.query(Valeur_Grandeur).get(id_valeur)
    if v:
        session.delete(v)
        session.commit()

def lire_valeurs_grandeur(id_grandeur=None):
    query = session.query(Valeur_Grandeur)
    if id_grandeur:
        query = query.filter_by(id_grandeur=id_grandeur)

    valeurs = query.all()
    for v in valeurs:
        print(f"[{v.id}] {v.nom} = {v.valeur} (grandeur {v.id_grandeur})")
    
    return valeurs

############################# Lien Onglet Grandeur #############################

def lier_onglet_grandeur(id_onglet, id_grandeur):
    session.execute(Onglet_Grandeur.insert().values(id_onglet=id_onglet, id_grandeur=id_grandeur))
    session.commit()

def supprimer_lien_onglet_grandeur(id_onglet, id_grandeur):
    session.execute(
        Onglet_Grandeur.delete().where(
            (Onglet_Grandeur.c.id_onglet == id_onglet) & 
            (Onglet_Grandeur.c.id_grandeur == id_grandeur)
        )
    )
    session.commit()

def lire_all_onglet_grandeurs():
    results = session.execute(Onglet_Grandeur.select()).fetchall()
    for row in results:
        print(f"Onglet ID: {row.id_onglet}, Grandeur ID: {row.id_grandeur}")
    return results

