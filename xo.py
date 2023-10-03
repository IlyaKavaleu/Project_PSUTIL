class XO:
    def __init__(self):
        print('Start game')

    def field_xo(self):
        name_1 = input('Enter yr name: ')
        name_2 = input('Enter yr name: ')
        numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        winner_flag = True
        winner_comb = [(1, 2, 3), (4, 5, 6), (7, 8, 9), (1, 4, 7), (2, 5, 8), (3, 6, 9), (1, 5, 9), (3, 5, 7)]
        while winner_flag:
            player_1 = int(input(f'Enter number {name_1}: '))
            if 1 <= player_1 < len(numbers) and numbers[player_1] != 0:
                numbers[player_1] = 'X'
                for comb in winner_comb:
                    if all(numbers[position] == 'X' for position in comb):
                        print(f"Winner player {name_1}!")
                        winner_flag = False
            else:
                print('Enter true number or this cell occupied.')
                continue

            player_2 = int(input(f'Enter number {name_2}: '))
            if 1 <= player_1 < len(numbers) and numbers[player_2] != 'X':
                numbers[player_2] = 0
                for comb in winner_comb:
                    if all(numbers[position] == 0 for position in comb):
                        print(f"Winner player {name_2}!")
                        winner_flag = False
            else:
                print('Enter true number or this cell occupied.')
                continue

            print("|\"\"\"\"\"\"\"||\"\"\"\"\"\"\"||\"\"\"\"\"\"\"|")
            print(f"|   {numbers[1]}   ||   {numbers[2]}   ||   {numbers[3]}   |")
            print("|_______||_______||_______|")
            print("|\"\"\"\"\"\"\"||\"\"\"\"\"\"\"||\"\"\"\"\"\"\"|")
            print(f"|   {numbers[4]}   ||   {numbers[5]}   ||   {numbers[6]}   |")
            print("|\"\"\"\"\"\"\"||\"\"\"\"\"\"\"||\"\"\"\"\"\"\"|")
            print(f"|   {numbers[7]}   ||   {numbers[8]}   ||   {numbers[9]}   |")
            print("|_______||_______||_______|")


xo = XO()
xo.field_xo()
