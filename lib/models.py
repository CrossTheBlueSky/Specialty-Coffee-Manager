from sqlalchemy import ForeignKey, Column, Integer, String, create_engine, func, UniqueConstraint, select
from sqlalchemy.orm import Session, DeclarativeBase, relationship

# definine Base with 2.0 syntax
class Base(DeclarativeBase):
    pass


# defining Roaster class
class Roaster(Base):
    __tablename__= "roasters"
    id = Column(Integer, primary_key = True)
    name = Column(String)
    location = Column(String)


# Roasters have a one to many relationship with their coffees and to the cafes they serve
    coffees = relationship("Coffee", back_populates='roaster')
    cafes = relationship("Cafe", back_populates="roaster")


# defining Coffee class
class Coffee(Base):
    __tablename__ = "coffees"
    id = Column(Integer, primary_key = True)
    name = Column(String)
    country_of_origin = Column(String)
    roast_level = Column(Integer)
    roaster_id = Column(Integer, ForeignKey('roasters.id'))


# Coffees have a many-to-one relationship with their roaster
# They have a many-to-many relationship to the cafes that serve them
    roaster = relationship("Roaster", back_populates = "coffees")
    cafes = relationship("CoffeeCafe", back_populates="coffee")


class Cafe(Base):
    __tablename__ = "cafes"
    id = Column(Integer, primary_key = True)
    name = Column(String)
    location = Column(String)
    specialty = Column(String)
    roaster_name = Column(String)
    roaster_id = Column(Integer, ForeignKey('roasters.id'))

# Cafes are only serviced by one roaster (many to one)
    roaster = relationship("Roaster", back_populates="cafes")

#But since they can have many coffees from that roaster, a join table is necessary (many-to-many)
    coffees = relationship("CoffeeCafe", back_populates="cafe")

# Join table for coffees and cafes, since a coffee can be served at many cafes
# and a cafe can serve many coffees
class CoffeeCafe(Base):
    __tablename__ = "coffee_cafe"
    id = Column(Integer, primary_key = True)
    cafe_id = Column(Integer, ForeignKey("cafes.id"))
    cafe_name = Column(String)
    coffee_id = Column(Integer, ForeignKey("coffees.id"))
    coffee_name = Column(String)
    roaster_name = Column(String)

    cafe = relationship("Cafe", back_populates="coffees")
    coffee = relationship("Coffee", back_populates="cafes")



engine = create_engine("sqlite:///specialty_coffee.db")