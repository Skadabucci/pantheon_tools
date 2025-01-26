from typing import Optional, List
from datetime import datetime
import json
from enum import Enum

GLOBAL_COOLDOWN = 1.1

class SpellType(Enum):
    USE = 1
    TECHNIQUE = 2
    UTILITY = 3

    @classmethod
    def from_input(cls, input_value: int):
        if input_value == 1:
            return cls.USE
        elif input_value == 2:
            return cls.TECHNIQUE
        elif input_value == 3:
            return cls.UTILITY
        else:
            raise ValueError("Invalid input for spell type")

    def __str__(self):
        return self.name.lower()
            
class Spell:
    def __init__(self, name: str, cast_time: float, type: str, location: int, cooldown: float = 0.0, has_gcd: bool = True):
        self.name: str = name
        self.cast_time: float = cast_time
        if type not in ["use", "technique", "utility"]:
            raise ValueError("type must be 'use', 'technique', or 'utility'")
        self.type: str = type
        self.location: int = location

        self.cooldown: float = cooldown
        self.has_gcd: bool = has_gcd

        self.last_cast: Optional[float] = None

    def add_to_last_cast(self, time: float):
        # If the last_cast is None it has never been cast so cannot be on cooldown
        if self.last_cast is not None:
            self.last_cast += time

class Spellbook:
    def __init__(self, class_name: str, spells: List[Spell], file_path: str = None):
        self.class_name: str = class_name
        self.spells: List[Spell] = spells
        self.file_path: str = file_path

    def add_spell(self, spell: Spell):
        self.spells.append(spell)

    def save_to_file(self, file_path: str = None):
        with open(file_path, 'w') as file:
            json.dump({
                "class_name": self.class_name,
                "spells": [{k: v for k, v in spell.__dict__.items() if k != 'last_cast'} for spell in self.spells]
            }, file, indent=4)
        print(f"Spellbook saved to {file_path}")
        
    @classmethod
    def load_from_file(cls, file_path: str):
        with open(file_path, 'r') as file:
            data = json.load(file)
            spells = [Spell(**spell_data) for spell_data in data["spells"]]
            return cls(data["class_name"], spells)
        
    def list_spells(self):
        print(f"{'id':<3}{'Name':<20}{'Cast Time':<15}{'Type':<15}{'Location':<10}{'Cooldown':<10}{'Has GCD':<10}")
        print("-" * 80)
        for i, spell in enumerate(self.spells):
            print(f"{i:<3}{spell.name:<20}{spell.cast_time:<15}{spell.type:<15}{spell.location:<10}{spell.cooldown:<10}{spell.has_gcd:<10}")

    def add_spells_interactively(self):
        while True:
            print("\nOptions:")
            print("  (q) Quit")
            print("  (L) List existing spells")
            print("  Create a new spell")
            option = input("Choose (q or L) or type name of spell: ")

            if option.lower() == 'q' or option.lower() == 'quit':
                break
            elif option.lower() == 'l' or option.lower() == 'list':
                self.list_spells()
                continue
            else:
                name = option
            
            cast_time = float(input("Enter cast time: "))
            type_input = int(input("Enter spell type (1: use, 2: technique, 3: utility): "))
            type = str(SpellType.from_input(type_input))
            location = int(input("Enter spell location: "))
            cooldown = float(input("Enter cooldown (default 0.0): ") or 0.0)
            has_gcd = input("Has global cooldown? (yes/no, default yes): ").lower() in ['yes', 'y', '']

            spell = Spell(name, cast_time, type, location, cooldown, has_gcd)
            self.add_spell(spell)
        
        self.save_to_file(self.file_path)

    def rank_spells(self):
        ranked_spells = []
        self.list_spells()
        print("\nRank the spells in order of importance by entering their IDs separated by spaces.")
        id_list_input = input("Enter the spell IDs in order of importance (space separated): ").split(" ")
        id_list = []
        for id in id_list_input:
            if id.strip():
                spell_id = int(id.strip())
                if spell_id in id_list:
                    print(f"Warning: Duplicate spell ID {spell_id} found and ignored.")
                else:
                    id_list.append(spell_id)

        for id in id_list:
            ranked_spells.append(self.spells[id])

        return ranked_spells

def create_new_spellbook(existing_file: Optional[str] = None):
    if existing_file:
        existing_spellbook = Spellbook.load_from_file(existing_file)
        spellbook = Spellbook(existing_spellbook.class_name, existing_spellbook.spells, existing_file)
    else:
        class_name = input("Enter the class name for the spellbook: ")
        file_path = input("Enter file path to save the spellbook: ")
        spellbook = Spellbook(class_name, [], file_path)

    spellbook.add_spells_interactively()
    return spellbook


def create_macro(spellbook: Spellbook):
    macro_lines = []
    macro_file = input("Enter the file path to save the macro: ")
    ranked_spells = spellbook.rank_spells()
    desired_spell_count = int(input("\nEnter the number of spells to include in the macro: "))
    number_of_spells = 0
    warning_printed = False
    
    while number_of_spells < desired_spell_count:
        current_spell_count = number_of_spells
        for spell in ranked_spells:
            if spell.last_cast is None or spell.last_cast >= spell.cooldown:
                max_delay = max(GLOBAL_COOLDOWN, spell.cast_time)
                macro_lines.append(f"/{spell.type} {spell.location}")
                macro_lines.append(f"/wait {max_delay:.1f}")
                for other_spell in ranked_spells:
                    if spell.name == other_spell.name:
                        spell.last_cast = 0.0 # Reset the last cast time
                    else:
                        other_spell.add_to_last_cast(max_delay)
                number_of_spells += 1
                break
        if current_spell_count == number_of_spells:
            if not warning_printed:
                print("Warning: No spells were able to cast in time. Please consider adding more spells to the macro to optimize dps.")
                warning_printed = True
            minimum_remaining_cast_time = 99.0
            for spell in ranked_spells:
                if spell.last_cast is None:
                    raise Exception("Spell has never been cast, cannot calculate remaining cast time. This is a bug.")
                minimum_remaining_cast_time = min(minimum_remaining_cast_time, spell.cooldown - spell.last_cast)
            prior_wait_time = float(macro_lines[-1].split(" ")[-1])
            macro_lines[-1] = f"/wait {prior_wait_time + minimum_remaining_cast_time:.1f}"
            for spell in ranked_spells:
                spell.add_to_last_cast(minimum_remaining_cast_time)

    with open(macro_file, 'w') as file:
        for line in macro_lines:
            file.write(line + "\n")
    print(f"Macro created and saved to {macro_file}")


def main():
    print("Please choose an option:")
    print("  1. Load from an existing file")
    print("  2. Start a new spellbook")
    choice = input("Enter 1, or 2: ")
    if choice == '1':
        existing_file = input("Enter the path of the existing spellbook file: ")
        spellbook = create_new_spellbook(existing_file)
    elif choice == '2':
        spellbook = create_new_spellbook()
    else:
        print("Invalid choice. Exiting.")
        return 1

    print("\nWould you like to create a macro? (y/n).")
    create_macro_choice = input("Enter y or n: ")
    if create_macro_choice.lower() == 'y':
        create_macro(spellbook)
        return 0
    else:
        print("Exiting.")
        return 0

if __name__ == "__main__":
    main()
