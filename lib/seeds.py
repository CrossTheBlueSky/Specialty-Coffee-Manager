from models import *
import random
from faker import Faker

if __name__ == '__main__':
    faker = Faker()


# Drops the tables and creates them again
    Coffee.__table__.drop(engine)
    Cafe.__table__.drop(engine)
    Roaster.__table__.drop(engine)
    CoffeeCafe.__table__.drop(engine)
    Base.metadata.create_all(engine)


# The "specialty" attribute is kinda unecessary, but since I have it I needed something to seed it.
    specialty_list = ["Concept Beverages", "Pourovers", "Single-Origin", "None"]

# establish session so things can actually be added to the db
    with Session(engine) as session:

# make 10 roasters and add to db
        for i in range(10):
            roaster = Roaster(
                name = f"{faker.word().capitalize()} {faker.word().capitalize()} Roastery",
                location = f"{faker.city()}, {faker.state()}"

            )
            session.add(roaster)
            session.commit()


# make 50 types of coffee and add to db
# applies 5 coffees to each roaster
        for i in range(50):
            current_roaster = int(i/5)+1
            if current_roaster > 10:
                current_roaster = 10
            coffee = Coffee(
                name = f"{faker.word().capitalize()} Blend",
                roast_level = random.randint(1, 10),
                country_of_origin = faker.country(),
                roaster_id = current_roaster,
                roaster_name = session.query(Roaster).filter(current_roaster == Roaster.id).first().name
            )
            session.add(coffee)
            session.commit()

        
# make 15 cafes and relate them to beans, then add to db
        for i in range(15):

            # Generates a random roaster to relate to the cafe
            # Variablized so it can be used to grab the name of the roaster
            # and for readability
            roaster_num = random.randint(1, 10)
            roaster_name = session.query(Roaster).filter(roaster_num == Roaster.id).first().name

            cafe = Cafe(
                name = f"The {faker.word().capitalize()} and {faker.word().capitalize()}",
                specialty = specialty_list[random.randint(0, 3)],
                location = f"{faker.city()}, {faker.state()}",
                roaster_name = f"{roaster_name}",
                roaster_id = roaster_num
            )
            session.add(cafe)
            session.commit()

            # Retrieves the list of coffees from the roaster assigned to the cafe
            coffee_list = session.query(Coffee).filter(Coffee.roaster_id == cafe.roaster_id).all()

            for j in range(3):
                # Chooses a random coffee from the roaster and relates it to the cafe
                coffee_num = random.randint(0, len(coffee_list) - 1)
                coffee = coffee_list[coffee_num]
                coffee_cafe = CoffeeCafe(
                    cafe_id = cafe.id,
                    cafe = cafe,
                    cafe_name = cafe.name,
                    coffee = coffee,
                    coffee_id = coffee.id,
                    coffee_name = coffee.name,
                    roaster_name = cafe.roaster.name
                )
                # Removes the coffee from the list so it can't be added to the same cafe twice
                coffee_list.remove(coffee_cafe.coffee)

                session.add(coffee_cafe)
                session.commit()


