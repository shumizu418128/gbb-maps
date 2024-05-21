from sqlalchemy import Column, Float, ForeignKey, Integer, String

from models.database import Base


class Country(Base):
    __tablename__ = 'countries'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    name_ja = Column(String, nullable=False, unique=True)
    lat = Column(Float, nullable=False, unique=True)
    lon = Column(Float, nullable=False, unique=True)
    iso_code = Column(Integer, nullable=False, unique=True)

    def __init__(self, name, name_ja, lat, lon, iso_code):
        self.name = name
        self.name_ja = name_ja
        self.lat = lat
        self.lon = lon
        self.iso_code = iso_code

    def __repr__(self):
        return f'<Country {self.country}>'


class Participant(Base):
    __tablename__ = 'participants'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    iso_code = Column(Integer, ForeignKey(
        'countries.iso_code'), nullable=False)
    members = Column(String)

    def __init__(self, name, category, iso_code, members=None):
        self.name = name
        self.category = category
        self.iso_code = iso_code
        self.members = members

    def __repr__(self):
        return f'<Participant {self.name}>'
