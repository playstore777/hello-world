# Write your code here
# 200 ml of water, 50 ml of milk, and 15 g of coffee beans.
# Write how many disposable cups of coffee do you want to add:
class CoffeeMachine:
    coffee_storage = {'water': 400, 'milk': 540, 'coffee_beans': 120, 'disposable_cups': 9, 'money': 550}
    machine_storage = coffee_storage.copy()

    def question(self, quantity, ingredients):
        print(f'Write how many {quantity} of {ingredients} do you want:')

    def machine_details(self, water, milk, coffee_beans, d_cups, money):
        print('\nThe coffee machine has:')
        print(f'{water} of water')
        print(f'{milk} of milk')
        print(f'{coffee_beans} of coffee beans')
        print(f'{d_cups} of disposable cups')
        print(f'{money} of money')

    def action(self, storage):
        print('\nWrite action (buy, fill, take, remaining, exit):')
        action_input = input()
        return action_input

    def buy(self, storage):
        print("What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino, back - to main menu:")
        action_buy = input()
        if action_buy == '1':
            # For one espresso, the coffee machine needs 250 ml of water and 16 g of coffee beans. It costs $4.
            if (storage['water'] - 250) >= 0 and (storage['coffee_beans'] - 16) >= 0 and (
                    storage['disposable_cups'] - 1) >= 0:
                storage['water'] -= 250
                storage['coffee_beans'] -= 16
                storage['money'] += 4
                storage['disposable_cups'] -= 1
                print('I have enough resources, making you a coffee!')
            else:
                if (storage['water'] - 250) <= 0:
                    word = 'water'
                elif (storage['coffee_beans'] - 16) <= 0:
                    word = 'coffee_beans'
                elif (storage['disposable_cups'] - 1) <= 0:
                    word = 'disposable cups'
                print(f"Sorry, not enough {word}")
        elif action_buy == '2':
            # For a latte, the coffee machine needs 350 ml of water, 75 ml of milk, and 20 g of coffee beans. It costs $7.
            if (storage['water'] - 350) >= 0 and (storage['milk'] - 75) >= 0 and (
                    storage['coffee_beans'] - 20) >= 0 and (storage['disposable_cups'] - 1) >= 0:
                storage['water'] -= 350
                storage['milk'] -= 75
                storage['coffee_beans'] -= 20
                storage['money'] += 7
                storage['disposable_cups'] -= 1
                print('I have enough resources, making you a coffee!')
            else:
                if (storage['water'] - 350) <= 0:
                    word = 'water'
                elif (storage['milk'] - 75) <= 0:
                    word = 'milk'
                elif (storage['coffee_beans'] - 20) <= 0:
                    word = 'coffee_beans'
                elif (storage['disposable_cups'] - 1) <= 0:
                    word = 'disposable cups'
                print(f"Sorry, not enough {word}")
        elif action_buy == '3':
            # And for a cappuccino, the coffee machine needs 200 ml of water, 100 ml of milk, and 12 g of coffee. It costs $6.
            if (storage['water'] - 200) >= 0 and (storage['milk'] - 100) >= 0 and (
                    storage['coffee_beans'] - 12) >= 0 and (storage['disposable_cups'] - 1) >= 0:
                storage['water'] -= 200
                storage['milk'] -= 100
                storage['coffee_beans'] -= 12
                storage['money'] += 6
                storage['disposable_cups'] -= 1
                print('I have enough resources, making you a coffee!')
            else:
                if (storage['water'] - 200) <= 0:
                    word = 'water'
                elif (storage['milk'] - 100) <= 0:
                    word = 'milk'
                elif (storage['coffee_beans'] - 12) <= 0:
                    word = 'coffee_beans'
                elif (storage['disposable_cups'] - 1) <= 0:
                    word = 'disposable cups'
                print(f"Sorry, not enough {word}")
        elif action_buy == 'back':
            return None
        return storage

    def fill(self, storage):
        self.question('ml', 'water')
        storage['water'] += int(input())

        self.question('ml', 'milk')
        storage['milk'] += int(input())

        self.question('grams', 'coffee_beans')
        storage['coffee_beans'] += int(input())

        self.question('disposable cups', 'coffee')
        storage['disposable_cups'] += int(input())

        return storage

    def take(self, storage):
        print(f'I gave you {storage["money"]}')
        storage['money'] -= storage['money']
        return storage

    def main(self):
        action_input = self.action(self.machine_storage)
        while action_input != exit:
            if action_input == 'buy':
                return_storage = self.buy(self.machine_storage)
                if return_storage != None:
                    self.machine_storage = return_storage
            elif action_input == 'fill':
                self.machine_storage = self.fill(self.machine_storage)
            elif action_input == 'take':
                self.machine_storage = self.take(self.machine_storage)
            elif action_input == 'remaining':
                self.machine_details(self.machine_storage["water"], self.machine_storage["milk"],
                                     self.machine_storage['coffee_beans'], self.machine_storage['disposable_cups'],
                                     self.machine_storage['money'])
            elif action_input == 'exit':
                break
            action_input = self.action(self.machine_storage)


coffee = CoffeeMachine()
coffee.main()