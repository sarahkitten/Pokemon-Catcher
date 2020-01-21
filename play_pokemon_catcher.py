"""
To play pokemon catching game using pokedict file
TODO:
add gens
add catch-all
"""

import sys
from dictfile_web import *

DEBUG = False


def log(s):
    if DEBUG:
        print(s)


def mon_str_validate(mon_str):
    mons_with_types = ["Lycanroc", "Nidoran", "Meowstic",
                       "Wormadam", "Deoxys", "Giratina",
                       "Shaymin", "Mimikyu", "Basculin",
                       "Darmanitan", "Thundurus",
                       "Landorus", "Tornadus", "Keldeo",
                       "Meloetta", "Aegislash", "Pumpkaboo",
                       "Gourgeist", "Oricorio", "Wishiwashi",
                       "Minior"]
    mons_with_dashes = ["Ho-oh", "Porygon-z", "Jangmo-o",
                        "Hakamo-o", "Kommo-o"]
    if '.' in mon_str:
        mon_str = mon_str.replace('.', '')
    if '-' in mon_str:
        words = mon_str.split('-')
        first = words[0]
        if first in mons_with_types:
            mon_str = first
        elif mon_str in mons_with_dashes:
            pass
        elif mon_str == 'Type-null':
            mon_str = 'Type:null'
        else:
            mon_str = None
    if mon_str:
        if 'Galarian' in mon_str:
            mon_str = None
    return mon_str


# def dictfile_to_dict():
#     """
#     Convert dictfile to dict
#     :return:
#     """
#     pokedict = {}
#     f = open("\share\pokeapp\pokedict.txt", "r")                                 # FIXME
#     for line in f:
#         entry = line.split(';')
#         pokedict[entry[0]] = entry[1].strip()
#     f.close()
#     return pokedict


# def add_splitter_for_web_version():
#     pokedict = {}
#     f = open("\share\pokeapp\pokedict.txt", "r")
#     g = open("\share\pokeapp\webpokedict.txt", "w+")
#     for line in f:
#         line = line.rstrip("\n\r")
#         g.write(f"{line}9")
#     f.close()
#     g.close()
#     return pokedict


def prune(pokedict):
    """
    uses mon_str_validate to prune pokeinfo list
    :param pokedict:
    :return:
    """
    pruned = {}
    for mon in pokedict:
        valid_name = mon_str_validate(mon)
        if valid_name:
            if valid_name not in pruned:
                pruned[valid_name] = pokedict[mon]
    return pruned


def make_pokedict():
    """
    Uses pokedict_maker functions to make pruned dictionary (name : p_type)
    :return:
    """
    pokedict = web_dictfile_to_dict()
    pokedict = prune(pokedict)
    log(f"Pokedict: {pokedict}")
    return pokedict


def make_catalog(pokedict, p_type):
    """
    Returns set of names of all pokemon of type p_type
    :param pokedict:
    :param p_type:
    :return:
    """
    catalog = set()
    for mon in pokedict:
        if p_type.capitalize() in pokedict[mon]:
            catalog.add(mon)
    log(f"Catalog: {catalog}")
    return catalog


def get_type():
    """
    prompts the user for a pokemon type,
    returns string p_type
    :return:
    """
    p_type = None
    while not p_type:
        inp = input("What type would you like to catch? ")
        if inp.lower() in ["normal", "fire", "fighting", "water", "flying",
                           "grass", "poison", "electric", "ground", "psychic",
                           "rock", "ice", "bug", "dragon", "ghost", "dark",
                           "steel", "fairy"]:
            p_type = inp
        else:
            print("Did you spell that right?", file=sys.stderr)
    return p_type


def give_up(catalog):
    """
    prints uncaught pokemon of type p_type, exits program
    :param catalog:
    :return:
    """
    print("You missed:")
    for mon_str in catalog:
        print(mon_str)
    input("Nice try")
    exit(0)


def main():
    # prep
    pokedict = make_pokedict()
    pokedex = set()
    complete = False

    # get type, make catalog
    p_type = get_type()
    catalog = make_catalog(pokedict, p_type)
    to_go = len(catalog)
    print(f"{to_go} {p_type} pokemon left.")

    # catch pokemon
    while not complete:
        mon_str = input("Catch a pokemon (q to give up): ").capitalize()
        if mon_str == "Q":
            give_up(catalog)

        if mon_str in pokedex:                         # already caught mon
            print(f"You already have {mon_str}!", file=sys.stderr)

        elif mon_str not in catalog:                    # wrong type
            if mon_str in pokedict:
                print(f'{mon_str} is {pokedict[mon_str]} type', file=sys.stderr)

            else:                                       # misspelling
                print("Did you spell that right?", file=sys.stderr)

        else:                                           # caught mon
            catalog.remove(mon_str)
            pokedex.add(mon_str)
            to_go -= 1
            if to_go != 0:
                print(f"You caught {mon_str}! {to_go} left!")
            else:  # caught all mons
                complete = True
                input(f"You caught all the {p_type} type pokemon!!")

    exit(0)


if __name__ == "__main__":
    main()

