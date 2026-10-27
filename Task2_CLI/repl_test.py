import cmd

class FoodREPL(cmd.Cmd):
    prompt = 'food_repl> '
    intro = 'Type "help" or "?" to list commands.\n'

    def __init__(self):
        # Initiate on superclass cmd.Cmd
        super().__init__()
        variables = {}

    def do_test(self, arg):
        'Print given argument:  TEST argument:str'
        if arg:
            print(f'Argument: {arg}')
        else:
            print(f'No arguments given.\n')

    def do_exit(self, arg):
        'Exit the application:  EXIT'
        print('Exiting the application.')
        return True
    do_x = do_exit



    


if __name__ == '__main__':
    FoodREPL().cmdloop()