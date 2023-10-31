class NotValidNamePlayer(Exception):
    """Ім'я користувача невалідне"""

    def __str__(self):
        return "\nІм'я введено невалідно."


class NotCellsBusy(Exception):
    """Відсутні вільні клітинки"""
    pass


class CellBusy(Exception):
    """Клітинка зайнята"""

    def __str__(self):
        return "\nКлітинка зайнята, оберіть іншу.\n"


class NotValidStep(TypeError):
    """Невалідний хід"""

    def __str__(self):
        return "\nВаш хід не валідний! Це повинно бути два числа через пробіл від 1 до 3"


class Cell:  # клас клітинки
    def __init__(self, coordinate):
        self.__cell = None  # маркер в клітинці Х або О
        self.__coordinate = coordinate

    @property
    def cell(self):
        return self.__cell

    @cell.setter
    def cell(self, marker):
        self.__cell = marker

    @property
    def coordinate(self):
        return self.__coordinate

    @coordinate.setter
    def coordinate(self, coordinate):
        self.__coordinate = coordinate

    def __bool__(self):
        return False if self.cell else True

    def __repr__(self):
        return self.cell if self.cell else '  '


class Field:  # клас поля
    def __init__(self, size_field=3):
        self.field = self.init_field(size_field)  # вкладений кортеж кожний елемент окремий рядок

    def __getitem__(self, item):
        return self.field[item]

    def __setitem__(self, key, value):
        row, col = key
        self.field[row][col].cell = value

    @staticmethod
    def init_field(size_field):  # ініціалізація поля необхідного розміру
        return [[Cell((x, y)) for y in range(size_field)] for x in range(size_field)]

    def check_free_field(self):  # перевірка поля на наявність пустих клітинок False - пусті клітинки є
        for row in self.field:
            if any(cell for cell in row):
                return False
        raise NotCellsBusy

    def check_free_cell(self, col, row):  # перевірка на те що клітинка без маркера
        return self.field[col][row]

    def cell_marker_field(self, coordinate, marker):  # змінює маркер в клітинці на маркер гравця
        col, row = coordinate
        if self.check_free_cell(col, row):
            self[coordinate] = marker
        else:
            raise CellBusy

    def __str__(self):  # відображення поля в консолі
        show_field = ''
        for col in self.field:
            for cell in col:
                show_field += cell.__repr__() + '|'
            show_field = show_field[:-1] + '\n'
        return show_field


class Player:  # клас гравця
    def __init__(self, name, marker):
        self.name = name  # ім'я гравця
        self.marker = marker  # маркер гравця
        self.steps = []

    def add_step(self, coordinate):  # додає хід гравця до списку зроблених ходів гравцем
        self.steps.append(coordinate)

    def __str__(self):
        return self.name


class GameController:
    win_combination = [
        [[0, 0], [0, 1], [0, 2]], [[0, 0], [1, 0], [2, 0]],
        [[0, 0], [1, 1], [2, 2]], [[0, 1], [1, 1], [2, 1]],
        [[0, 2], [1, 1], [2, 0]], [[0, 2], [1, 2], [2, 2]],
        [[1, 0], [1, 1], [1, 2]], [[2, 0], [2, 1], [2, 2]]
    ]

    def __init__(self, player_1, player_2, field):
        self.player_1 = player_1
        self.player_2 = player_2
        self.field = field
        self.current_player = player_1

    def switch_player(self):  # визначення хто ходить
        self.current_player = self.player_2 if self.current_player == self.player_1 else self.player_1

    def make_move(self, coordinate):
        try:
            self.field.cell_marker_field(coordinate, self.current_player.marker)
            self.current_player.add_step(coordinate)
        except CellBusy as e:
            print(e)
            return False
        return True

    @classmethod
    def check_win(cls, player):  # перевірка чи має гравець виграшну комбінацію
        for combination in cls.win_combination:
            if all(comb in player.steps for comb in combination):
                return True
        return False

    @staticmethod
    def validate_step(move_input):  # перевірка ходу на валідність
        try:
            step = [int(i) for i in move_input.split()]
            if all(i in range(1, 4) for i in step):
                return [i - 1 for i in step]
            raise NotValidStep
        except (TypeError, ValueError, NotValidStep):
            print(NotValidStep())

    def play_game(self):
        while True:
            print(self.field)
            player = self.current_player
            print(f'Гравець {player}, ваш хід!')
            coordinate = self.validate_step(input('Введіть координати (рядок та стовпець, від 1 до 3) через пробіл: '))
            if self.make_move(coordinate):
                if self.check_win(player):
                    print(self.field)
                    print(f"Гравець {player} виграв!")
                    break
                if self.field.check_free_field():
                    print(self.field)
                    print("Нічия!")
                    break
                self.switch_player()


class Play:  # клас гри
    def __new__(cls, *args, **kwargs):
        print("******** Вітаємо у грі хрестики - нолики! ********\n")
        return object.__new__(cls)

    def __init__(self):
        self.player_1 = Player(self.input_player_name('X'), marker='❎')
        self.player_2 = Player(self.input_player_name('O'), marker='🔴')
        self.field = Field()
        self.game_controller = GameController(self.player_1, self.player_2, self.field)

    def input_player_name(self, marker):  # старт нової гри
        print(f"Введіть ім'я гравця, який буде грати за -{marker}- та натисніть Enter")
        try:
            return self.validate_player_name(input('Введіть ім\'я: '))
        except NotValidNamePlayer as e:
            print(e)
            return self.input_player_name(marker)

    @staticmethod  # перевірка на валідність імені граця
    def validate_player_name(name):
        if isinstance(name, str) and name:
            return name
        raise NotValidNamePlayer

    def __call__(self, *args, **kwargs):
        self.game_controller.play_game()


if __name__ == '__main__':
    game = Play()
    game()
