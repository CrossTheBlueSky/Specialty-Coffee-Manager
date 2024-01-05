from models import *
import inquirer
from prettytable.colortable import ColorTable

if __name__ == '__main__':

# Welcomes the user and establishes a session
    with Session(engine) as session:
        print(ascii)
        print("Hello, Weird Coffee Person!")
        print("Welcome to your Specialty Coffee Manager")

# all menus using 2.0 syntax (select-scalars) instead of 1.4 syntax (query)
# may refactor seeds and models to do the same. If so, this comment should be deleted
        
# Get all roasters from the database
        
        def get_roasters():
            roaster_list = session.scalars(select(Roaster))
            roaster_table = ColorTable()
            roaster_table.field_names = ["ID", "Name", "Location", "Coffees Provided"]
            for roaster in roaster_list:
                coffee_string = ""
                for coffee in roaster.coffees:
                    if(coffee_string == ""):
                        coffee_string += f"{coffee.name}"
                    else:
                        coffee_string += f", {coffee.name}"
                roaster_table.add_row([roaster.id, roaster.name, roaster.location, coffee_string])
            print(roaster_table)

# Get all coffees from the database
            
        def get_coffees():
            coffee_list = session.scalars(select(Coffee))
            coffee_table = ColorTable()
            coffee_table.field_names = ["ID","Name", "Roast Level", "Country of Origin", "Roasted By", "Served At"]
            for coffee in coffee_list:
                cafe_string = "Direct Order Only"
                for rel in coffee.cafes:
                    if(cafe_string == "Direct Order Only"):
                        cafe_string = f"{rel.cafe_name}"
                    else:
                        cafe_string += f", {rel.cafe_name}"
                coffee_table.add_row([coffee.id, coffee.name, coffee.roast_level, coffee.country_of_origin, coffee.roaster.name, cafe_string])
            print(coffee_table)

# Get all cafes from the database
            
        def get_cafes():
           cafe_list = session.scalars(select(Cafe))
           cafe_table = ColorTable()
           cafe_table.field_names = ["ID", "Name", "Address", "Roaster", "Specialty", "Coffees Served"]
           for cafe in cafe_list:
                coffee_string = ""
                for coffee in cafe.coffees:
                   if(coffee_string == ""):
                    coffee_string += f"{coffee.coffee_name}"
                   else:
                        coffee_string += f", {coffee.coffee_name}"
                cafe_table.add_row([cafe.id, cafe.name, cafe.location, cafe.roaster_name, cafe.specialty, coffee_string])
           print(cafe_table)
           

# Roaster Menu asks for user input and calls the appropriate function

        def roaster_menu():
            roaster_question = [inquirer.List('roaster_menu', 
                                              message="What would you like to do?",
                                              choices=['Add Roaster', 'Edit Roaster', 'Remove Roaster', 'Go Back'],
                                              carousel = True,),]
            roaster_response = inquirer.prompt(roaster_question)
            if(roaster_response['roaster_menu'] == "Go Back"):
                intro()
            elif(roaster_response['roaster_menu'] == "Add Roaster"):
                add_roaster()
            elif(roaster_response['roaster_menu'] == "Edit Roaster"):
                edit_roaster()
            elif(roaster_response['roaster_menu'] == "Remove Roaster"):
                remove_roaster()

# Add Roaster asks for basic roaster info, then calls roast_beans to add coffees to the roaster
        
        def add_roaster():
            name = input("What is the name of the roastery?")
            location = input("Where are they located?")
            new_roaster = Roaster(
                name = name,
                location = location
            )
            session.add(new_roaster)
            session.commit()
            print(f"{new_roaster.name} needs to start roasting some coffee!")
            roast_beans(new_roaster)
            get_roasters()
            print(f"{new_roaster.name} added!")
            roaster_menu()

# roast_beans asks for coffee info, then adds it to the database with a relationship 
# to the roaster passed from add_roaster
        
        def roast_beans(roaster):
            coffee_list = []
            while True:
                name = input("What is the name of the roast?")
                roast_level = int(input("What is the roast level on a scale of 1-10, with 1 being the lightest and 10 being the darkest?"))
                if roast_level not in range(1, 11):
                    while True:
                        print("Invalid Input. Please enter a number between 1 and 10")
                        roast_level = int(input("What is the roast level on a scale of 1-10, with 1 being the lightest and 10 being the darkest?"))
                        if roast_level in range(1, 11):
                            break
                country = input("In which country were the beans grown?")
                new_coffee = Coffee(
                    name = name,
                    roast_level = roast_level,
                    country_of_origin = country,
                    roaster_id = roaster.id
                )
                coffee_list.append(new_coffee)
                session.add(new_coffee)
                session.commit()
                print(f"{new_coffee.name} added!")
                finished = input("Is this all the coffee you want to add? Y/N")
                if finished.upper() == "Y":
                    break
            print(f"{roaster.name} is now roasting:")
            for coffee in coffee_list:
                print(coffee.name)
            
# Edits roaster info
        
        def edit_roaster():
            roaster_id = int(input("Using the id from the table above, which roaster would you like to edit?"))
            current_roaster = session.query(Roaster).filter(Roaster.id == roaster_id).first()
            while True:
                new_name = input(f"What is the new name of this roastery? (Currently {current_roaster.name})")
                new_location = input(f"What is the new location? (Currently {current_roaster.location})")
                print(new_name) 
                print(new_location) 
                finished = input(f"Is this correct? Y/N")
                if finished.upper() == "Y":
                    break
# Waits for confirmation before updating the roaster
            current_roaster.name = new_name
            current_roaster.location = new_location
            session.add(current_roaster)
            session.commit()
            get_roasters()
            print(f"{current_roaster.name} updated!")
            roaster_menu()

# Removes roaster from database. If cafes are affected, 
# calls find_new_roaster to update them

        def remove_roaster():
            response = int(input("Using the id from the table above, which roaster would you like to delete? (Enter 0 to cancel)"))
            while True:
                if response == 0:
                    get_roasters()
                    roaster_menu()
                    break
                else:
                    to_delete = session.query(Roaster).filter(Roaster.id == response).first()
                    effected_cafes = session.query(Cafe).filter(Cafe.roaster_id == to_delete.id).all()
                    confirm = input(f"Delete {to_delete.name}? Y/N")
                    if confirm.upper() == "Y":
                        session.delete(to_delete)
                        session.commit()
                        get_roasters()
                        print("Cafes that served this roaster must be updated!")
                        for cafe in effected_cafes:
                            find_new_roaster(cafe)
                        break
                    elif confirm.upper() == "N":
                        get_roasters()
                        roaster_menu()
                        break
            get_roasters()
            print(f"{to_delete.name} deleted!")
            roaster_menu()

# Updates cafes that were affected by the removal of a roaster, or adds a roaster to a new cafe
        
        def find_new_roaster(cafe):
            roaster_list = session.query(Roaster).all()
            print("Please choose a new roaster from the list below")
            for roaster in roaster_list:
                print(f"{roaster.id} - {roaster.name}")
            new_roaster = None
            while True:
                new_roaster = input(f"Using the id from the list above, which roaster would you like to select? (Selecting for {cafe.name})")
                roaster_check = session.query(Roaster).filter(Roaster.id == new_roaster).first() or None
                if roaster_check != None:
                    cafe.roaster_id = new_roaster
                    cafe.roaster_name = session.query(Roaster).filter(Roaster.id == new_roaster).first().name
                    break
                else:
                    print("Invalid Input. Please pick a roaster from the list above")
            session.add(cafe)
            session.commit()
            print(f"{cafe.name} now serves {cafe.roaster_name}")
            restock_coffee(cafe)

# Restocks coffee for a cafe after a new roaster is selected

        def restock_coffee(cafe):
            coffee_list = session.query(Coffee).filter(Coffee.roaster_id == cafe.roaster_id).all()
            old_coffee = session.query(CoffeeCafe).filter(CoffeeCafe.cafe_id == cafe.id).all()
            
            if len(old_coffee) > 0:
                for coffee in old_coffee:
                    session.delete(coffee)
                    session.commit()
            while True:
                for coffee in coffee_list:
                    print(f"{coffee.id} - {coffee.name}")
                choice = input("Using the IDs above, select one coffee that this cafe serves (or enter 0 to finish selecting)")
                if choice.isdigit() == True:
                    choice = int(choice)
                if choice == 0:
                    break
                while session.query(Coffee).filter(Coffee.id == choice).first() not in coffee_list:
                    for coffee in coffee_list:
                        print(f"{coffee.id} - {coffee.name}")
                    print("Invalid Input. Please select a coffee from the list above")
                    choice = input("Using the IDs above, select one coffee that this cafe serves (or enter 0 to finish selecting)")
                    if choice.isdigit() == True:
                        choice = int(choice)
                    if choice == 0:
                        break
                else:
                    selected_coffee = session.query(Coffee).filter(Coffee.id == choice).first()
                    coffee_cafe = CoffeeCafe(
                        cafe = cafe,
                        cafe_name = cafe.name,
                        coffee = selected_coffee,
                        coffee_name = selected_coffee.name,
                        roaster_name = cafe.roaster.name
                    )

                    coffee_list.remove(coffee_cafe.coffee)
                    print(f"{coffee_cafe.coffee_name} Added to {cafe.name}")
                    session.add(coffee_cafe)
                    session.commit()

# Coffee Menu asks for user input and calls the appropriate function

        def coffee_menu():
            coffee_question = [inquirer.List('coffee_menu', 
                                              message="What would you like to do?",
                                              choices=['Add Coffee', 'Remove Coffee', 'Edit Coffee', 'Go Back'],
                                              carousel = True,),]
            coffee_response = inquirer.prompt(coffee_question)
            if coffee_response['coffee_menu'] == "Go Back":
                intro()
            elif coffee_response['coffee_menu'] == "Add Coffee":
                add_coffee()
            elif coffee_response['coffee_menu'] == "Remove Coffee":
                delete_coffee()
            elif coffee_response['coffee_menu'] == "Edit Coffee":
                edit_coffee()

# asks for coffee info and adds it to the database

        def add_coffee():
            name = input("What is the name of the roast?")
            roast_level = input("What is the roast level on a scale of 1-10, with 1 being the lightest and 10 being the darkest? (Whole numbers only, 0 to cancel)")
            if roast_level == 0:
                get_coffees()
                coffee_menu()
            while roast_level.isdigit() == False or int(roast_level) not in range(1, 11):
                print("Invalid Input. Please enter a whole number between 1 and 10")
                roast_level = input("What is the roast level on a scale of 1-10, with 1 being the lightest and 10 being the darkest? (Whole numbers only, 0 to cancel)")
            country = input("In which country were the beans grown?")
            get_roasters()
            roaster = input("Using their id from the list above, which roastery provides this coffee?")
            roaster_check = session.query(Roaster).filter(Roaster.id == roaster).first() or None
            while roaster_check == None:
                print("Invalid Input. Please pick a roaster from the list above")
                roaster = input("Using their id from the list above, which roastery provides this coffee?")
                roaster_check = session.query(Roaster).filter(Roaster.id == roaster).first() or None

            new_coffee = Coffee(
                name = name,
                roast_level = roast_level,
                country_of_origin = country,
                roaster_id = roaster
            )
            session.add(new_coffee)
            session.commit()
            get_coffees()
            print(f"{new_coffee.name} added!")
            coffee_menu()

# Edits coffee info
        
        def edit_coffee():
            coffee_id = int(input("Using the id from the table above, which coffee would you like to edit?"))
            current_coffee = session.query(Coffee).filter(Coffee.id == coffee_id).first()
            old_roaster = current_coffee.roaster_id
            while True:
                new_name = input(f"What is the new name of this roast? (Currently {current_coffee.name})")
                new_level = input(f"What is the new roast level? (Currently {current_coffee.roast_level})")
                while new_level.isdigit() == False or int(new_level) not in range(1, 11):
                    print("Invalid Input. Please enter a whole number between 1 and 10")
                    new_level = input(f"What is the new roast level? (Currently {current_coffee.roast_level})")

                new_country = input(f"What is the new country of origin (Currently {current_coffee.country_of_origin})")
                get_roasters()
                new_roaster = input(f"Using their id above, select the roaster who produces this coffee (Currently {current_coffee.roaster_id} - {current_coffee.roaster.name})")
                roaster_check = session.query(Roaster).filter(Roaster.id == new_roaster).first() or None
                while roaster_check == None:
                    input("Invalid Input. Please pick a roaster from the list above")
                    new_roaster = input("Using their id from the list above, which roastery provides this coffee?")
                    roaster_check = session.query(Roaster).filter(Roaster.id == new_roaster).first() or None
                
                roaster_name = session.query(Roaster).filter(Roaster.id == new_roaster).first().name
                print(new_name) 
                print(f"Roast Level - {new_level}") 
                print(new_country) 
                print(f"{roaster_name}")
                finished = input(f"Is this correct? Y/N")
                if finished.upper() == "Y":
                    break
# Waits for confirmation before updating the coffee
            current_coffee.name = new_name
            current_coffee.roast_level = new_level
            current_coffee.country_of_origin = new_country
            current_coffee.roaster_id = new_roaster
            if new_roaster != old_roaster:
                rels = session.query(CoffeeCafe).filter(CoffeeCafe.coffee_id == current_coffee.id).all()
                for rel in rels:
                    session.delete(rel)
                    session.commit()
            session.add(current_coffee)
            session.commit()
            get_coffees()
            print(f"{current_coffee.name} updated!")
            coffee_menu()

# Removes coffee from database.

        def delete_coffee():
            response = int(input("Using the id from the table above, which coffee would you like to delete? (Enter 0 to cancel)"))
            while True:
                if response == 0:
                    get_coffees()
                    coffee_menu()
                    break
                else:
                    to_delete = session.query(Coffee).filter(Coffee.id == response).first()
                    confirm = input(f"Delete {to_delete.name}? Y/N")
                    if confirm.upper() == "Y":
                        session.delete(to_delete)
                        session.commit()
                        get_coffees()
                        print(f"{to_delete.name} deleted!")
                        coffee_menu()
                        break

# Cafe Menu asks for user input and calls the appropriate function

        def cafe_menu():
            cafe_question = [inquirer.List('cafe_menu', 
                                              message="What would you like to do?",
                                              choices=['Add Cafe', 'Remove Cafe', 'Edit Cafe', 'Go Back'],
                                              carousel = True,),]
            cafe_response = inquirer.prompt(cafe_question)
            if cafe_response['cafe_menu'] == "Go Back":
                intro()
            elif cafe_response['cafe_menu'] == "Add Cafe":
                add_cafe()
            elif cafe_response['cafe_menu'] == "Edit Cafe":
                edit_cafe()
            elif cafe_response['cafe_menu'] == "Remove Cafe":
                remove_cafe()

# Asks for cafe info and adds it to the database, 
# then calls find_new_roaster to add a roaster and coffees to the cafe
        def add_cafe():
            name = input("What is the name of the cafe?")
            location = input("Where are they located?")
            specialty = input("What is their specialty? (Or type 'None' if they don't have one)")
            new_cafe = Cafe(
                name = name,
                location = location,
                specialty = specialty,
            )

            session.add(new_cafe)
            session.commit()
            find_new_roaster(new_cafe)
            get_cafes()
            print(f"{new_cafe.name} added!")
            cafe_menu()
            
# Edits cafe info
            
        def edit_cafe():
            get_cafes()
            cafe_id = input("Using the id from the table above, which cafe would you like to edit? (Or enter 0 to go back)")
            while cafe_id.isdigit() == False or session.query(Cafe).filter(Cafe.id == cafe_id).first() == None:
                cafe_id = input("Invalid Input. Please enter a cafe id from the table above")
            if cafe_id == 0:
                get_cafes()
                cafe_menu()
            current_cafe = session.query(Cafe).filter(Cafe.id == cafe_id).first()
            old_roaster = current_cafe.roaster_id
            while True:
                new_name = input(f"What is the new name of this cafe? (Currently {current_cafe.name})")
                new_location = input(f"What is the new location? (Currently {current_cafe.location})")
                new_specialty = input(f"What is the new specialty? (Currently {current_cafe.specialty})")
                get_roasters()
                new_roaster = input(f"Using their id above, select the roaster who services this cafe (Currently {current_cafe.roaster_id} - {current_cafe.roaster.name})")
                roaster_check = session.query(Roaster).filter(Roaster.id == new_roaster).first() or None
                while roaster_check == None:
                    input("Invalid Input. Please pick a roaster from the list above")
                    new_roaster = input(f"Using their id from the list above, select the roaster who services this cafe? (Currently {current_cafe.roaster_id} - {current_cafe.roaster.name})")
                    roaster_check = session.query(Roaster).filter(Roaster.id == new_roaster).first() or None
                
                roaster_name = session.query(Roaster).filter(Roaster.id == new_roaster).first().name
                print(new_name) 
                print(new_location) 
                print(new_specialty) 
                print(f"{roaster_name}")
                finished = input(f"Is this correct? Y/N")
                if finished.upper() == "Y":

# waits for confirmation before updating the cafe
                    
                    current_cafe.name = new_name
                    current_cafe.location = new_location
                    current_cafe.specialty = new_specialty
                    current_cafe.roaster_id = new_roaster
                    current_cafe.roaster_name = roaster_name

                    session.add(current_cafe)
                    session.commit()
                    break
# if the roaster has changed, calls restock_coffee to update the cafe's coffees
            if old_roaster != new_roaster:
                print("Coffees served by this cafe must be updated!")
                restock_coffee(current_cafe)

            get_cafes()
            print(f"{current_cafe.name} updated!")
            cafe_menu()

# Removes cafe from database.

        def remove_cafe():
            response = input("Using the id from the table above, which cafe would you like to delete? (Enter 0 to cancel)")
            while response.isdigit() == False or session.query(Cafe).filter(Cafe.id == response).first() == None:
                response = input("Invalid Input. Please enter a cafe id from the table above")
            response = int(response)
            while True:
                if response == 0:
                    get_cafes()
                    cafe_menu()
                    break
                else:
                    to_delete = session.query(Cafe).filter(Cafe.id == response).first()
                    confirm = input(f"Delete {to_delete.name}? Y/N")
                    if confirm.upper() == "Y":
                        session.delete(to_delete)
                        session.commit()
                        get_cafes()
                        print(f"{to_delete.name} deleted!")
                        cafe_menu()
                        break
                    else:
                        get_cafes()
                        cafe_menu()
                        break

# Gives the user the option to view cafes, roasters, or coffees, or exit the program
                    
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



                
        

