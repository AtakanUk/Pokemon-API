import requests
from .util import *

def get_ability_description(ability_url):
    response = requests.get(ability_url)

    if response.status_code == 200:
        data = response.json()
        for effect_entry in data['effect_entries']:
            if effect_entry['language']['name'] == 'en':
                return split_long_text(effect_entry['short_effect'])

    return None

def retrieve_pokemon_data(pokemon_name):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    return None

def get_pokemon_abilities(data):
    abilities = []
    for ability_data in data['abilities']:
        ability_name = ability_data['ability']['name']
        ability_url = ability_data['ability']['url']
        description = get_ability_description(ability_url)
        if description:
            abilities.append([ability_name, description])
    return abilities
