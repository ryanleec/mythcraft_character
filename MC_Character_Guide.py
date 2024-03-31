import os
import json

#print("Global attributes initialized:", attributes)

# Function to clear the screen
def clear_screen():
    if os.name == 'nt':  # Check if operating system is Windows
        os.system('cls')
    else:
        os.system('clear')

# Placeholder ASCII Art
def display_ascii_art():
    print("** Placeholder ASCII Art **")

# Introduction 
def display_intro():
    print("Welcome to the Character Creation Guide!")
    print("let's begin by selecting your lineage.")
    
def load_lineages(filename="lineage_data.json"):
    with open(filename, "r") as f:
        return json.load(f)

def display_lineages(lineage_data):
    print("\nAvailable Lineages:")
    for i, lineage_name in enumerate(lineage_data):
        print(f"{i+1}. {lineage_name}")

def select_lineage(lineage_data):
    while True:
        display_lineages(lineage_data)
        try:
            choice = int(input("Select your lineage: "))
            if 0 < choice <= len(lineage_data):
                selected_lineage_name = list(lineage_data.keys())[choice - 1]
                return selected_lineage_name, lineage_data[selected_lineage_name]
            else:
                print("Invalid selection. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def display_abilities(abilities):
    for ability_name, ability_desc in abilities.items():
        if ability_name != 'sublineages':  # Skip the 'sublineages' key
            print(f"- {ability_name}: {ability_desc}")
        else:  # We've found the sublineages section
            for sublineage_name, sublineage_abilities in ability_desc.items():
                print(f"\nSublineage: {sublineage_name}")  # Print sublineage header
                for sub_ability_name, sub_ability_desc in sublineage_abilities.items():
                    print(f"- {sub_ability_name}: {sub_ability_desc}")

def select_sublineage(sublineages):
    if sublineages:  # Check if any sublineages exist
        print("\nAvailable Sublineages:")
        for i, sublineage_name in enumerate(sublineages):
            print(f"{i+1}. {sublineage_name}")
        while True:    
            try:
                choice = int(input("Select your sublineage: "))
                if 0 < choice <= len(sublineages):
                    return list(sublineages.keys())[choice - 1]
                else:
                    print("Invalid selection. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")
    else:
        return None  # No sublineages exist
    
def display_attributes(attributes, remaining_points):  # No need for copy
    print("Attribute Points Remaining:", remaining_points)
    print("Select the attribute to modify:")
    for i, (abbr, value) in enumerate(attributes.items()):  # Use attributes directly 
        print(f"{i+1}. {abbr}: {value}")

def get_attribute_choice():
    print("Attributes in get_attribute_choice:", character['attributes'])
    while True:
        try:
            choice = int(input("Enter the number of the attribute to modify: "))
            if 1 <= choice <= 8:  
                return choice - 1  # Convert to list index
            else:
                print("Invalid choice. Please select a number between 1 and 8.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    #print("attributes at the end of get_attribute_choice:", attributes)

def get_attribute_value(remaining_points):
    print("Entering get_attribute_value")
    while True:
        try:
            value = int(input("Enter the value to add or subtract: "))
            if -3 <= value <= 2 and remaining_points + value >= 0:  
                return value  # Return the value if valid
            else:
                print("Invalid value or not enough points remaining.") 
        except ValueError:
            print("Invalid input. Please enter a number.")

def set_attributes(character, remaining_points):
    #print("Attributes at start of set_attributes:", character["attributes"])  # Check initial values 
    
    while remaining_points != 0:
        print("Remaining Points:", remaining_points)
        display_attributes(character["attributes"], remaining_points)  # Pass in correct reference
        choice = get_attribute_choice() 
        value = get_attribute_value(remaining_points)

        print("Validating Value:", value, "Remaining Points:", remaining_points) 
        if -3 <= value <= 2 and remaining_points + value >= 0:  # Check valid value and point limits
            print("Choice returned from function:", choice)
            print("Selected Attribute Index:", choice - 1)
           
            # Error Handling
            print("Attributes Dictionary:", character["attributes"])  # For debugging
            if character["attributes"].get(str(choice - 1)) is None: # Convert to string
                print("Error: Attribute not initialized")
            else:
                #print("Attributes before modification:", character["attributes"])
                character["attributes"][choice - 1] += value  # Modify the attribute directly
                print("New Value:", character["attributes"][choice - 1]) # Print the value after
                remaining_points -= value
        else:
            print("Invalid input. Please try again.")
    #print("Attributes at end of set_attributes:", character["attributes"])  # Check finished values

# Main Logic
if __name__ == "__main__":
    remaining_points = 5
    print("remaining_points at start of main loop:", remaining_points)
    clear_screen()
    display_ascii_art()
    display_intro()

    # Initialize 'character' dictionary only once
    character = {
        "lineage": "",
        "attributes": {
            "STR": 0,
            "DEX": 0,
            "END": 0,
            "AWR": 0,
            "INT": 0,
            "CHA": 0,
            "LUCK": 0,
            "COR": 0
        }
    }
    lineage_data = load_lineages()

print("Character dictionary before lineage loop:", character)

while "lineage" not in character: 
   lineage_name, lineage_abilities = select_lineage(lineage_data)  
   print(f"\nYou've selected: {lineage_name}")
   display_abilities(lineage_abilities)

   selected_sublineage = select_sublineage(lineage_abilities.get('sublineages'))

   if input("Confirm this lineage? (yes/no): ").lower() == 'yes':
       character["lineage"] = lineage_name
       if selected_sublineage:  # Only add 'sublineage' if one was selected
           character["sublineage"] = selected_sublineage
       print("Lineage confirmed!")
       break  
   else:
       clear_screen()
            
set_attributes(character, remaining_points)
print("Attributes after set_attributes:", character['attributes'])