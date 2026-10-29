import cmd, shlex, requests, json
import urllib.parse
import pandas as pd
from bs4 import BeautifulSoup

def get_data(code):
    headers = {'User-Agent': 'School Food Research App - V1.0 - clarkb@pedarecc.sa.edu.au'}
    # Escapes every special character
    code_safe = urllib.parse.quote(code, safe='')
    response = requests.get(f'https://world.openfoodfacts.org/api/v2/product/{code_safe}', headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data['status'] == 1:
            print(f'Successfully retrieved data for product: {data.get('product', {}).get('product_name')}\n')
        else:
            print(f'Error getting data: {data.get('status_verbose', 'unkown')}\n')
        return data
    else:
        print(response.url)
        print(f'Error {response.status_code}: {response.text}')
        return {}

def get_product_search(search_terms):
    url = "https://search.openfoodfacts.org/search"
    # Headers identify the script to the server
    # Prevents getting blocked by servers that reject the default Python identifier
    headers = {'User-Agent': 'School Food Research App - V1.0 - clarkb@pedarecc.sa.edu.au'}
    params = {'q': search_terms,
              'fields': 'product_name,code,categories,ingredients_text',
              'size': 10}
    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        print(response.url)
        data = response.json()
        hits = data.get('hits', [])
        return hits
    else:
        print(response.url)
        print(f'Error {response.status_code}: {response.text}')
    return []

def get_allergens(data):
    ingredients_text = str(data.get('product', {}).get('ingredients_text_with_allergens'))
    # Use Python's built in HTML parser
    soup = BeautifulSoup(ingredients_text, 'html.parser')
    # Text allergens are typically highlighted with <span>
    allergens = soup.find_all('span')
    allergens_text = ', '.join([allergen.get_text() for allergen in allergens])
    allergens_text = allergens_text if allergens_text else 'none'
    return allergens_text

class FoodREPL(cmd.Cmd):
    prompt = 'food_app> '
    intro = 'Enter "help" or "?" to list commands.\n'

    def __init__(self):
        # Wait for superclass cmd.Cmd initiation
        super().__init__()
        # self.code = 3017620422003
        # with open('output_example.json', 'r', encoding='utf-8') as file:
        #     data = json.load(file)
        # self.data = data
        # self.name = 'Nutella
        self.code = None
        self.data = {}
        self.name = 'None'
        self.nutri_stats = {'Energy': {'value': 'energy_100g', 'unit': 'energy_unit'},
                            'Fats': {'value': 'fat_100g', 'unit': 'fat_unit'},
                            'Sat Fats': {'value': 'saturated-fat_100g', 'unit': 'saturated-fat_unit'},
                            'Sodium': {'value': 'sodium_100g', 'unit': 'sodium_unit'},
                            'Carbs': {'value': 'carbohydrates_100g', 'unit': 'carbohydrates_unit'},
                            'Sugars': {'value': 'sugars_100g', 'unit': 'sugars_unit'},
                            'Proteins': {'value': 'proteins_100g', 'unit': 'proteins_unit'}}
        self.nutri_score_desc = {'a': 'Excellent choice: Very high nutritional quality for this type of food.\nIdeal for daily consumption.',
                                 'b': 'Good choice: Good overall nutritional quality for this type of food.\nHealthy option that can be eaten regularly.',
                                 'c': 'Moderate choice: Balanced nutritional quality for this type of food.\nConsume in moderation as part of a varied diet.',
                                 'd': 'Limited choice: Low nutritional quality for this type of food.\nConsume less frequently and in smaller portions.',
                                 'e': 'Occasional choice: Very low nutritional quality for this type of food.\nReserve as an occasional treat.'}
        self.search = 'None'
        self.search_results = pd.DataFrame()

    def _update_state(self, arg):
        args = shlex.split(arg)
        if len(args) > 0:
            self.code = args[0]
            self.data = get_data(self.code)
            self.name = self.data.get('product', {}).get('product_name')

    def do_exit(self, arg):
        'Exit the application:  EXIT'
        print('Exiting the application.\n')
        return True
    do_x = do_exit

    def do_code(self, arg):
        'Set current code to given code:  CODE code:int\nWarning: Passing code into other commands will override the current code.'
        args = shlex.split(arg)
        if len(args) == 0:
            print(self.code)
            print()
        else:
            self.code = args[0]
            print(f'Current code set to {self.code}\n')

    def do_getdata(self, arg):
        'Get and set data for given code:  GETDATA code:int\nLeave blank to get data for current code.'
        args = shlex.split(arg)
        if len(args) > 0:
            self.code = args[0]
        self.data = get_data(self.code)
        self.name = self.data.get('product', {}).get('product_name')

    def do_dumpdata(self, arg):
        'Dump current data to "output.json":  DUMPDATA'
        try:
            with open('output.json', 'w') as file:
                json.dump(self.data, file, indent=4)
            print('Data output successfully.\n')
        except:
            print('Error writing to file.\n')

    def do_name(self, arg):
        'Get product name for given code:  NAME code:int\nLeave blank to get name for current data.\nLeave blank to get current code.'
        self._update_state(arg)
        print(f'Product name: {self.name}\n')

    def do_categories(self, arg):
        'Get categories for given code:  CATEGORIES code:int\nLeave blank to get categories for current data.'
        self._update_state(arg)
        categories = self.data.get('product', {}).get('categories')
        print(f'{self.name} categories: {categories}\n')

    def do_ingredients(self, arg):
        'Get ingredients for given code:  INGREDIENTS code:int\nLeave blank to get ingredients for current data.'
        self._update_state(arg)
        ingredients = self.data.get('product', {}).get('ingredients_text')
        print(f'{self.name} ingredients: {ingredients}')
        allergens = get_allergens(self.data)
        print(f'Allergens: {allergens}\n')

    def do_nutriinfo(self, arg):
        'Get nutritional information per 100g for given code:  NUTRIINFO code:int\nLeave blank to get nutrition for current data.'
        self._update_state(arg)
        nutri_data = self.data.get('product', {}).get('nutriments', {})
        nutri_info = {'Stat': [],
                      'Value': [],
                      'Unit': []}
        nutri_stats = self.nutri_stats
        for stat in nutri_stats:
            nutri_info['Stat'].append(stat)
            nutri_info['Value'].append(nutri_data.get(nutri_stats[stat]['value']))
            nutri_info['Unit'].append(nutri_data.get(nutri_stats[stat]['unit']))
        nutri_dataframe = pd.DataFrame(nutri_info)
        print(f'Nutrional information for {self.name} (100g)')
        print(nutri_dataframe.to_string(index=False))
        print()

    def do_nutriscore(self, arg):
        'Get Nutri-Score for given code:  NUTRISCORE code:int\nLeave blank to get Nutri-Score for current data.\nThe Nutri-Score compares the nutrional value of products in the same categories.'
        self._update_state(arg)
        nutri_score = self.data.get('product', {}).get('nutriscore_grade')
        print(f'{self.name} Nutri-Score: {str(nutri_score).upper()}')
        print(self.nutri_score_desc.get(nutri_score))
        print()

    def do_dietary(self, arg):
        'Get allergens and available labels (e.g. gluten free) for given code:  DIETARY code:int\nLeave blank to get dietary information for current data.'
        self._update_state(arg)
        allergens = get_allergens(self.data)
        print(f'Allergen ingredients for {self.name}: {allergens}')
        labels = self.data.get('product', {}).get('labels')
        print(f'Labels: {labels}\n')

    def do_search(self, arg):
        'Get products and codes for given search terms:  SEARCH terms:string\nLeave blank to get previous search results.'
        if arg:
            results_data = get_product_search(arg)
            results = {'Name': [],
                        'Code': [],
                        'Categories': []}
            for result in results_data:
                results['Name'].append(result.get('product_name'))
                results['Code'].append(result.get('code'))
                results['Categories'].append(result.get('categories'))
            results_dataframe = pd.DataFrame(results)
            print(f'Search results for {arg}')
            # Printing dataframes automatically truncates values (such as categories)
            print(results_dataframe)
            print()
            self.search = arg
            self.search_results = results_dataframe
        else:
            print(f'Previous search results for {self.search}')
            print(self.search_results)
            print()


if __name__ == '__main__':
    FoodREPL().cmdloop()