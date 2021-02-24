class Coffee():  # Coffee class

    def __init__(self):  # Constructor
        self.water = 400
        self.milk = 540
        self.beans = 120
        self.cups = 9
        self.money = 550

    def remaining(self):
        print('The Coffee Machine has :')
        print(str(self.water) + ' ml of water')
        print(str(self.milk) + ' ml of milk')
        print(str(self.beans) + ' gm of coffee beans')
        print(str(self.cups) + ' of cups')
        print(str(self.money) + '$ of money')

    def buy(self):
        print('What do you want to buy ?\n 1. esspresso\n 2. lattee \n 3. cuppacino ')
        select = input()
        if select == '1':
            if self.water < 250:
                print('Sorry! I do not have water to make coffee ')
            elif self.beans < 16:
                print('Sorry! I do not have beans to make coffee')
            elif self.cups < 1:
                print('Sorry! I do not have cups to serve coffee')
            else:
                print('I have enough resources to make coffee')
                self.water -= 250
                self.beans -= 16
                self.cups -= 1
                self.money -= 4
        elif select == '2':
            if self.water < 350:
                print('Sorry! I do not have water to make coffee ')
            elif self.milk < 75:
                print('Sorry, I do not enough milk!')
            elif self.beans < 20:
                print('Sorry! I do not have beans to make coffee')
            elif self.cups < 1:
                print('Sorry! I do not have cups to serve coffee')
            else:
                print('I have enough resources to make coffee')
                self.water -= 350
                self.milk -= 75
                self.beans -= 20
                self.cups -= 1
                self.money -= 7
        elif select == '3':
            if self.water < 200:
                print('Sorry! I do not have water to make coffee ')
            elif self.milk < 100:
                print('Sorry, I do not enough milk!')
            elif self.beans < 12:
                print('Sorry! I do not have beans to make coffee')
            elif self.cups < 1:
                print('Sorry! I do not have cups to serve coffee')
            else:
                print('I have enough resources to make coffee')
                self.water -= 200
                self.milk -= 100
                self.beans -= 12
                self.cups -= 1
                self.money -= 8
        elif select == 'back':
            return


    def fill(self):
        print('Write how many ml of water do you want to add:')
        self.water += int(input())
        print('Write how many ml of milk do you want to add:')
        self.milk += int(input())
        print('Write how many grams of coffee beans do you want to add:')
        self.beans += int(input())
        print('Write how many disposable cups of coffee do you want to add:')
        self.cups += int(input())


    def take(self):
        print('I gave you $' + str(self.money))


    def menu(self):
        while True:
            print('Write action (buy, fill, take, remaining, exit):')
            action = input()
            if action == 'remaining':
                machine.remaining()
            elif action == 'fill':
                machine.fill()
            elif action == 'take':
                machine.take()
            elif action == 'buy':
                machine.buy()
            elif action == 'exit':
                break


machine = Coffee()
machine.menu()