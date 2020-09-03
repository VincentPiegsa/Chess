import pygame
from tools import load_image, render_text


class Figure(object):

    def __init__(self, row, column, color, filename):

        self.row = row
        self.column = column

        self.color = color
        self.filename = filename
        self.image = load_image(f'{self.filename}_{self.color}.png')

        self.width, self.height = self.image.get_rect().size
        self.has_moved = False
        self.value = 0

    def __repr__(self):

        return f'Figure: ({self.row}|{self.column}) <{self.color}>'

    def render(self, surface, position, tile_dimensions):

        x = position[0] + (self.column * tile_dimensions[0]) + (tile_dimensions[0] - self.width) // 2
        y = position[1] + (self.row * tile_dimensions[1]) + (tile_dimensions[1] - self.height) // 2

        surface.blit(self.image, (x, y))

    def paths(self, n_tiles, figure_map):

        return []

    def check_boundaries(self, pos, n_tiles):

        if pos[0] >= 0 and pos[0] < n_tiles:

            if pos[1] >= 0 and pos[1] < n_tiles:
                return True

        return False

    def move(self, row, column):

        self.row = row
        self.column = column

    def get_team(self):

        return self.color


class Pawn(Figure):

    def __init__(self, row, column, color):

        super().__init__(row, column, color, 'pawn')
        self.value = 1

    def move(self, row, column):

        self.row = row
        self.column = column

    def paths(self, n_tiles, figure_map):

        paths_list = []
        attack_list = []

        if self.has_moved:
            if self.color == 'white':
                potential_paths = [(self.row + 1, self.column)]
                potential_attack_paths = [(self.row + 1, self.column + 1),
                                          (self.row + 1, self.column - 1)]

            elif self.color == 'black':
                potential_paths = [(self.row - 1, self.column)]
                potential_attack_paths = [(self.row - 1, self.column + 1),
                                          (self.row - 1, self.column - 1)]

        else:
            if self.color == 'white':
                potential_paths = [(self.row + 1, self.column), (self.row + 2, self.column)]
                potential_attack_paths = [(self.row + 1, self.column + 1),
                                          (self.row + 1, self.column - 1)]

            elif self.color == 'black':
                potential_paths = [(self.row - 1, self.column), (self.row - 2, self.column)]
                potential_attack_paths = [(self.row - 1, self.column + 1),
                                          (self.row - 1, self.column - 1)]

        for potential_path in potential_paths:

            if self.check_boundaries(potential_path, n_tiles) and figure_map[potential_path[0]][potential_path[1]] == None:
                    paths_list.append(potential_path)

        for potential_path in potential_attack_paths:

                if self.check_boundaries(potential_path, n_tiles) and figure_map[potential_path[0]][potential_path[1]] != None and figure_map[potential_path[0]][potential_path[1]].color != self.color:
                    attack_list.append(potential_path)

        return paths_list, attack_list

    def paths_(self, n_tiles, figure_map):

        ''' DEPRECATED '''

        paths_list = []
        attack_list = []

        if self.color == 'white':
            potential_paths = [(self.row + 1, self.column),
                               (self.row + 1, self.column + 1),
                               (self.row + 1, self.column - 1)]

        elif self.color == 'black':
            potential_paths = [(self.row - 1, self.column),
                               (self.row - 1, self.column + 1),
                               (self.row - 1, self.column - 1)]

        for potential_path in potential_paths:

            if self.check_boundaries(potential_path, n_tiles):
                paths_list.append(potential_path)

        return paths_list


class Rook(Figure):

    def __init__(self, row, column, color):

        super().__init__(row, column, color, 'rook')
        self.value = 5

    def paths(self, n_tiles, figure_map):

        paths_list = []
        attack_list = []

        directions = [(+1, 0),
                      (-1, 0),
                      (0, +1),
                      (0, -1)]

        for direction in directions:

            n = 1
            while True:
                potential_path = (self.row + n * direction[0], self.column + n * direction[1])

                if self.check_boundaries(potential_path, n_tiles):

                    if figure_map[potential_path[0]][potential_path[1]] != None and figure_map[potential_path[0]][potential_path[1]].color == self.color:
                        break

                    elif figure_map[potential_path[0]][potential_path[1]] != None and figure_map[potential_path[0]][potential_path[1]].color != self.color:
                        attack_list.append(potential_path)

                        break

                    elif figure_map[potential_path[0]][potential_path[1]] == None:
                        paths_list.append(potential_path)

                        n += 1

                else:
                    break

        return paths_list, attack_list

    def paths_(self, n_tiles, figure_map):

        ''' DEPRECATED '''

        paths_list = []
        attack_list = []

        for n in range(1, n_tiles):

            potential_paths = [(self.row + n, self.column),
                               (self.row - n, self.column),
                               (self.row, self.column + n),
                               (self.row, self.column - n)]

            for potential_path in potential_paths:

                if self.check_boundaries(potential_path, n_tiles):
                    paths_list.append(potential_path)

        return paths_list, attack_list


class Knight(Figure):

    def __init__(self, row, column, color):

        super().__init__(row, column, color, 'knight')
        self.value = 3

    def paths(self, n_tiles, figure_map):

        paths_list = []
        attack_list = []

        potential_paths = [(self.row + 2, self.column + 1),
                (self.row + 2, self.column - 1),
                (self.row - 2, self.column + 1),
                (self.row - 2, self.column - 1),
                (self.row + 1, self.column + 2),
                (self.row + 1, self.column - 2),
                (self.row - 1, self.column + 2),
                (self.row - 1, self.column - 2)]

        for potential_path in potential_paths:

            if self.check_boundaries(potential_path, n_tiles):

                if figure_map[potential_path[0]][potential_path[1]] == None:
                    paths_list.append(potential_path)

                elif figure_map[potential_path[0]][potential_path[1]] != None and figure_map[potential_path[0]][potential_path[1]].color != self.color:
                    attack_list.append(potential_path)

        return paths_list, attack_list


class Bishop(Figure):

    def __init__(self, row, column, color):

        super().__init__(row, column, color, 'bishop')
        self.value = 3

    def paths(self, n_tiles, figure_map):

        paths_list = []
        attack_list = []

        directions = [(+1, +1),
                      (-1, -1),
                      (+1, -1),
                      (-1, +1)]

        for direction in directions:

            n = 1
            while True:

                potential_path = (self.row + n * direction[0], self.column + n * direction[1])

                if self.check_boundaries(potential_path, n_tiles):
                    if figure_map[potential_path[0]][potential_path[1]] != None and figure_map[potential_path[0]][potential_path[1]].color == self.color:
                        break

                    elif figure_map[potential_path[0]][potential_path[1]] != None and figure_map[potential_path[0]][potential_path[1]].color != self.color:
                        attack_list.append(potential_path)
                        break

                    elif figure_map[potential_path[0]][potential_path[1]] == None:
                        paths_list.append(potential_path)
                        n += 1

                else:
                    break

        return paths_list, attack_list

    def paths_(self, n_tiles, figure_map):

        ''' DEPRECATED '''

        paths_list = []
        attack_list = []

        for n in range(1, n_tiles):

            potential_paths = [(self.row + n, self.column + n),
                               (self.row - n, self.column - n),
                               (self.row + n, self.column - n),
                               (self.row - n, self.column + n)]

            for potential_path in potential_paths:

                if self.check_boundaries(potential_path, n_tiles):
                    paths_list.append(potential_path)

        return paths_list, attack_list


class Queen(Figure):

    def __init__(self, row, column, color):

        super().__init__(row, column, color, 'queen')
        self.value = 9

    def paths(self, n_tiles, figure_map):

        paths_list = []
        attack_list = []

        directions = [(+1, 0),
                      (-1, 0),
                      (0, +1),
                      (0, -1),
                      (+1, +1),
                      (-1, -1),
                      (+1, -1),
                      (-1, +1)]

        for direction in directions:

            n = 1
            while True:

                potential_path = (self.row + n * direction[0], self.column + n * direction[1])

                if self.check_boundaries(potential_path, n_tiles):

                    if figure_map[potential_path[0]][potential_path[1]] != None and figure_map[potential_path[0]][potential_path[1]].color == self.color:
                        break

                    elif figure_map[potential_path[0]][potential_path[1]] != None and figure_map[potential_path[0]][potential_path[1]].color != self.color:
                        attack_list.append(potential_path)
                        break

                    elif figure_map[potential_path[0]][potential_path[1]] == None:
                        paths_list.append(potential_path)
                        n += 1

                else:
                    break

        return paths_list, attack_list

    def paths_(self, n_tiles, figure_map):

        ''' DEPRECATED '''

        paths_list = []
        attack_list = []

        for n in range(1, n_tiles):

            potential_paths = [(self.row + n, self.column),
                               (self.row - n, self.column),
                               (self.row, self.column + n),
                               (self.row, self.column - n),
                               (self.row + n, self.column + n),
                               (self.row - n, self.column - n),
                               (self.row + n, self.column - n),
                               (self.row - n, self.column + n)]

            for potential_path in potential_paths:

                if self.check_boundaries(potential_path, n_tiles):
                    paths_list.append(potential_path)

        return paths_list, attack_list


class King(Figure):

    def __init__(self, row, column, color):

        super().__init__(row, column, color, 'king')
        self.value = 100

    def paths(self, n_tiles, figure_map):

        paths_list = []
        attack_list = []

        potential_paths = [(self.row + 1, self.column),
                           (self.row - 1, self.column),
                           (self.row, self.column + 1),
                           (self.row, self.column - 1),
                           (self.row + 1, self.column + 1),
                           (self.row + 1, self.column - 1),
                           (self.row - 1, self.column + 1),
                           (self.row - 1, self.column - 1)]

        for potential_path in potential_paths:

            if self.check_boundaries(potential_path, n_tiles):

                if figure_map[potential_path[0]][potential_path[1]] == None:
                    paths_list.append(potential_path)

                elif figure_map[potential_path[0]][potential_path[1]] != None and figure_map[potential_path[0]][potential_path[1]].color != self.color:
                    attack_list.append(potential_path)

        return paths_list, attack_list
