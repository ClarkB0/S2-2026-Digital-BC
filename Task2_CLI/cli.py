import cmd, shlex, requests, json

def get_data(code):
    try:
        data = requests.get(f'https://world.openfoodfacts.net/api/v2/product/{code}').json()
        if data['status'] == 1:
            print(f'Successfully retrieved data for product: {data['product']['product_name']}')
        else:
            print(f'Error getting data: {data['status_verbose']}')
        return data
    except:
        print('Error getting data: check network or URL')
        return None

class FoodREPL(cmd.Cmd):
    prompt = 'food_repl> '
    intro = 'Enter "help" or "?" to list commands.\n'

    def __init__(self):
        # Wait for superclass cmd.Cmd initiation
        super().__init__()
        self.barcode = '3017624010701' # Default barcode for development: Nutella
        self.data = None

    def do_exit(self, arg):
        'Exit the application:  EXIT'
        print('Exiting the application.')
        return True
    do_x = do_exit

    def do_barcode(self, arg):
        args = shlex.split(arg)
        if len(args) == 0:
            print(self.barcode)
        else:
            self.barcode = args[0]
            print(f'Barcode set to {self.barcode}')

    def do_getdata(self, arg):
        args = shlex.split(arg)
        if len(args) == 0:
            self.data = get_data(self.barcode)
        else:
            self.data = get_data(args[0])

    def do_dumpdata(self, arg):
        with open('output.json', 'w') as file:
            json.dump(self.data, file, indent=4)

    def do_ingredients(self, arg):
        args = shlex.split(arg)
        if len(args) == 0:
            pass




if __name__ == '__main__':
    FoodREPL().cmdloop()