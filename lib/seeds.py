from models import *
import random
from faker import Faker
from sqlalchemy import inspect, select


if __name__ == '__main__':
    faker = Faker()


# Check if the tables exist before dropping them
    # inspector = inspect(engine)
    # if inspector.has_table('coffee') and inspector.has_table('cafe') and inspector.has_table('roaster') and inspector.has_table('coffee_cafe'):
    Coffee.__table__.drop(engine)
    Cafe.__table__.drop(engine)
    Roaster.__table__.drop(engine)
    CoffeeCafe.__table__.drop(engine)
    Base.metadata.create_all(engine)


# The "specialty" attribute is kinda unecessary, but since I have it I needed something to seed it.
    specialty_list = ["Concept Beverages", "Pourovers", "Single-Origin", "None"]

# establish session so things can actually be added to the db
    with Session(engine) as session:

# make 20 roasters and add to db
        for i in range(20):
            roaster = Roaster(
                name = f"{faker.word().capitalize()} {faker.word().capitalize()} Roastery",
                location = faker.address()

            )
            session.add(roaster)
            session.commit()


# make 50 types of coffee and add to db
        for i in range(50):
            coffee = Coffee(
                name = f"{faker.word().capitalize()} Blend",
                roast_level = random.randint(1, 10),
                country_of_origin = faker.country(),
                roaster_id = random.randint(1, 20)
            )
            session.add(coffee)
            session.commit()

        
# make 30 cafes and relate them to beans, then add to db
        for i in range(30):

            # Generates a random roaster to relate to the cafe
            # Variablized so it can be used to grab the name of the roaster
            # and for readability
            roast_num = random.randint(1, 20)
            roast_name = session.query(Roaster).filter(roast_num == Roaster.id).first().name

            cafe = Cafe(
                name = f"The {faker.word().capitalize()} and {faker.word().capitalize()}",
                specialty = specialty_list[random.randint(0, 3)],
                location = faker.address(),
                roaster_name = f"{roast_name}",
                roaster_id = random.randint(1, 20)
            )
            session.add(cafe)
            session.commit()

            # Generates the list of coffees from a particular roaster
            coffee_list = session.query(Coffee).filter(Coffee.roaster_id == cafe.roaster_id).all()

            for j in range(4):
                # Confirms that there are coffees from that roaster
                if len(coffee_list) > 0:
                # Chooses a random coffee from the roaster and relates it to the cafe
                    coffee_num = random.randint(0, len(coffee_list) - 1)
                    coffee = coffee_list[coffee_num]
                    coffee_cafe = CoffeeCafe(
                        cafe = cafe,
                        cafe_name = cafe.name,
                        coffee = coffee,
                        coffee_name = coffee.name,
                        roaster_name = cafe.roaster.name
                    )
                # Removes the coffee from the list so it can't be added to the same cafe twice
                    coffee_list.remove(coffee_cafe.coffee)

                # If there are no coffees from that roaster, it breaks the loop
                else:
                    break

                session.add(coffee_cafe)
                session.commit()


