# Specialty-Coffee-Manager
Track specialty coffees, the roasters that provide them, and the cafes that sell them.

# How to use
1. Make sure you have python and pipenv installed on your system
2. Navigate to the specialty-coffee-manager directory in the terminal
3. Run the command `pipenv install` and then open a shell enrivonment using `pipenv shell`
4. With the shell environment open, enter the command 'python3 lib/app.py'

# Managing Coffee
When managing coffee, a roaster association is required. With this in mind, it is important to add a Roaster BEFORE adding a coffee that is produced by that roaster. Aside from this, coffees are the simplest thing to track, as changing or removing any given coffee doesn't have any significant impact on a Cafe or Roaster.

# Managing Roasters
When creating a new Roaster, you will be prompted to provide what their offerings are. It is possible for some roasteries to be currently out-of-stock, or freshly opened, so the control flow allows for a roaster to be created and the process of adding coffees to be skipped.

Since roasters relationships are managed in the classes they associate with (Coffee and Cafe, respectively), a roaster can be safely edited without needing to repair or replace any data.

When deleting a roaster, any cafe that serves product from that roaster will need to be updated with a new roaster. Additionally, they will need to be provided with coffees to serve from that roaster. The app will go through each cafe affected by a deleted rooaster, prompting the user to update the relationships that were removed.

# Managing Cafes
When creating a Cafe, a roaster will need to be assigned. If the cafe self-roasts or the roaster that services them is new, the new roaster (or the cafe themselves, added as a roastery) will need to be added BEFORE the cafe is created.

When editing a cafe, if the roaster is changed, the user will be prompted to select new coffees from the updated roaster to stock the cafe

The loss of a cafe doesn't directly effect any other relationships, so can be done safely. The only exception to this is if the coffee is a self-roaster, and is added as a roaster and a cafe before the deletion. This will NOT delete the cafe from the roasters menu. In order to completely remove a self-roasting cafe, they will need to be deleted separately from the Cafes menu and the Roasters menu.