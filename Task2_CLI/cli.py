import cmd, shlex, requests, json
import pandas as pd

def get_data(code):
    try:
        data = requests.get(f'https://world.openfoodfacts.net/api/v2/product/{code}').json()
        if data['status'] == 1:
            print(f'Successfully retrieved data for product: {data.get('product', {}).get('product_name')}')
        else:
            print(f'Error getting data: {data.get('status_verbose', {})}')
        return data
    except:
        print('Error getting data: check network or URL')
        return {}

class FoodREPL(cmd.Cmd):
    prompt = 'food_repl> '
    intro = 'Enter "help" or "?" to list commands.\n'

    def __init__(self):
        # Wait for superclass cmd.Cmd initiation
        super().__init__()
        self.code = '3017624010701' # Default code for development: Nutella
        with open('output_example.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        self.data = data
        self.name = 'Nutella'

    def do_exit(self, arg):
        'Exit the application:  EXIT'
        print('Exiting the application.')
        return True
    do_x = do_exit

    def do_code(self, arg):
        'Set current code to given code:  CODE code:int\nWarning: Passing code into other commands will override the current code.'
        args = shlex.split(arg)
        if len(args) == 0:
            print(self.code)
        else:
            self.code = args[0]
            print(f'code set to {self.code}')

    def do_getdata(self, arg):
        'Get and set data for given code:  GETDATA code:int\nLeave blank to get data for current code.'
        args = shlex.split(arg)
        if len(args) > 0:
            self.code = args[0]
        self.data = get_data(self.code)

    def do_dumpdata(self, arg):
        'Dump current data to output.json:  DUMPDATA'
        with open('output.json', 'w') as file:
            json.dump(self.data, file, indent=4)

    def do_name(self, arg):
        'Get product name for given code:  NAME code:int\nLeave blank to get name for current data.'
        args = shlex.split(arg)
        if len(args) > 0:
            self.code = args[0]
            self.data = get_data(self.code)
            self.name = self.data.get('product', {}).get('product_name')
        print(f'Product name: {self.name}')

    def do_ingredients(self, arg):
        'Get ingredients for given code:  INGREDIENTS code:int\nLeave blank to get ingredients for current data.'
        args = shlex.split(arg)
        if len(args) > 0:
            self.code = args[0]
            self.data = get_data(self.code)
            self.name = self.data.get('product', {}).get('product_name')
        ingredients = self.data.get('product', {}).get('ingredients_text')
        print(f'{self.name} ingredients: {ingredients}')

    def do_nutriinfo(self, arg):
        'Get nutritional information for given code:  NUTRIINFO code:int\nLeave blank to get nutrition for current data.'
        args = shlex.split(arg)
        if len(args) > 0:
            self.code = args[0]
            self.data = get_data(self.code)
        

if __name__ == '__main__':
    FoodREPL().cmdloop()