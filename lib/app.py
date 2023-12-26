from models import *
import inquirer
from prettytable.colortable import ColorTable

if __name__ == '__main__':


    with Session(engine) as session:
        print("Hello, Weird Coffee Person!")
        print("Welcome to your Specialty Coffee Manager")

# all menus using 2.0 syntax (select-scalars) instead of 1.4 syntax (query)
# may refactor seeds and models to do the same. If so, this comment should be deleted
        def get_roasters():
            roaster_list = session.scalars(select(Roaster))
            roaster_table = ColorTable()
            roaster_table.field_names = ["Name", "Location", "Coffees Provided"]
            for roaster in roaster_list:
                coffee_string = ""
                for coffee in roaster.coffees:
                    if(coffee_string == ""):
                        coffee_string += f"{coffee.name}"
                    else:
                        coffee_string += f", {coffee.name}"
                roaster_table.add_row([roaster.name, roaster.location, coffee_string])
            print(roaster_table)
        
        def get_coffees():
            coffee_list = session.scalars(select(Coffee))
            coffee_table = ColorTable()
            coffee_table.field_names = ["Name", "Roast Level", "Country of Origin", "Roasted By", "Served At"]
            for coffee in coffee_list:
                cafe_string = "Direct Order Only"
                for rel in coffee.cafes:
                    if(cafe_string == "Direct Order Only"):
                        cafe_string = f"{rel.cafe_name}"
                    else:
                        cafe_string += f", {rel.cafe_name}"
                coffee_table.add_row([coffee.name, coffee.roast_level, coffee.country_of_origin, coffee.roaster.name, cafe_string])
            print(coffee_table)

        def get_cafes():
           cafe_list = session.scalars(select(Cafe))
           cafe_table = ColorTable()
           cafe_table.field_names = ["Name", "Address", "Roaster", "Specialty", "Coffees Served"]
           for cafe in cafe_list:
                coffee_string = ""
                for coffee in cafe.coffees:
                   if(coffee_string == ""):
                    coffee_string += f"{coffee.coffee_name}"
                   else:
                        coffee_string += f", {coffee.coffee_name}"
                cafe_table.add_row([cafe.name, cafe.location, cafe.roaster_name, cafe.specialty, coffee_string])
           print(cafe_table)

        def roaster_menu():
            roaster_question = [inquirer.List('roaster_menu', 
                                              message="What would you like to do?",
                                              choices=['Add Roaster', 'Edit Roaster', 'Remove Roaster', 'Go Back'],
                                              carousel = True,),]
            roaster_response = inquirer.prompt(roaster_question)
            if(roaster_response['roaster_menu'] == "Go Back"):
                intro()

        def coffee_menu():
            coffee_question = [inquirer.List('coffee_menu', 
                                              message="What would you like to do?",
                                              choices=['Add Coffee', 'Remove Coffee', 'Edit Coffee', 'Go Back'],
                                              carousel = True,),]
            coffee_response = inquirer.prompt(coffee_question)
            if(coffee_response['coffee_menu'] == "Go Back"):
                intro()
        
        def cafe_menu():
            cafe_question = [inquirer.List('cafe_menu', 
                                              message="What would you like to do?",
                                              choices=['Add Cafe', 'Remove Cafe', 'Edit Cafe', 'Go Back'],
                                              carousel = True,),]
            cafe_response = inquirer.prompt(cafe_question)
            if(cafe_response['cafe_menu'] == "Go Back"):
                intro()

        def intro():
            intro_question =   [inquirer.List('main_menu',
                    message="What would you like to do?",
                    choices=['View Cafes', 'View Roasters', 'View Coffees', 'Exit'],
                    carousel=True,),]
            intro_response = inquirer.prompt(intro_question)


            if intro_response['main_menu'] == "View Cafes":
                get_cafes()
                cafe_menu()

            elif intro_response['main_menu'] == "View Roasters":
                get_roasters()
                roaster_menu()


            elif intro_response['main_menu'] == "View Coffees":
                get_coffees()
                coffee_menu()

        intro()



                
        

