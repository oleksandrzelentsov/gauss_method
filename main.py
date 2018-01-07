MATRIX = [
    [1, -3, 2, 3],
    [1, 1, -2, 1],
    [2, -1, 1, -1],
]


class Matrix():

    def __init__(self, n):
        self.n = n
        self.elements = []
        self.result = [0,] * self.n

        for row in range(n):
            self.elements.append([])
            for column in range(n):
                self.elements[row].append(0)

    @staticmethod
    def generate_matrix(n):
        elements = []
        for row in range(n):
            elements.append([])
            for column in range(n):
                elements[row].append(0)

        return elements

    def input(self):
        for row in range(self.n):
            for column in range(self.n):
                self.elements[row][column] = float(input('element[{}][{}]: '.format(row, column)))

            self.result[row] = float(input('result[{}]: '.format(row)))

    def input_from_list(self, matrix):
        for row in range(self.n):
            for column in range(self.n):
                self.elements[row][column] = matrix[row][column]

            self.result[row] = matrix[row][self.n]

    def output(self):
        for row in range(self.n):
            for column in range(self.n):
                print('{}'.format(self.elements[row][column]), end='  ')

            print('| {}'.format(self.result[row]))
        print()

    # def output(self):
    #    for row in self.element:
    #        for element in row:
    #            print(' {} '.format(element, end=''))
    #        print()

    def inverse_transpose(self):
        # self.elements[]
        tr_result = self.generate_matrix(self.n)
        for row, r_row in zip(range(self.n), range(self.n)[::-1]):
            for column, r_column in zip(range(self.n), range(self.n)[::-1]):
                tr_result[r_row][r_column] = self.elements[row][column]

        self.elements = tr_result
        self.result = self.result[::-1]

    def swap_column(self, column0, column1):
        for row in range(self.n):
            self.elements[row][column0], self.elements[row][column1] =\
                self.elements[row][column1], self.elements[row][column0]

    def swap_row(self, row0, row1):
        for column in range(self.n):
            self.elements[row0][column], self.elements[row1][column] =\
                self.elements[row1][column], self.elements[row0][column]

        self.result[row0], self.result[row1] = self.result[row1], self.result[row0]

    def cut_the_matrix(self, start_of_matrix):
        cutted_matrix = []
        for row in range(self.n):
            if row >= start_of_matrix:
                cutted_matrix.append(self.elements[row][start_of_matrix:self.n])
        return cutted_matrix

    def index_of_max_count(self, matrix, start_of_matrix):
        max_counts_in_rows = []

        for row in matrix:
            max_counts_in_rows.append(max(row))

        max_count = max(max_counts_in_rows)
        #       if max_count = 0:
        #            print('na przekatnej wystapil 0')
        #            return
        index_of_row_with_max_count = max_counts_in_rows.index(max_count) + start_of_matrix

        return (
            index_of_row_with_max_count,
            self.elements[index_of_row_with_max_count].index(max_count)  # index of column with max count
        )

    #    def swap_swaped_colums(self,swaped_columns)
    #        for columns in range(swaped_columns, 0, -1):

    def find_max_element_and_put_it_in_step(self):
        self.elements = sorted(self.elements, key=lambda row: max(row))[::-1]

    def gauss_with_swaping_columns_and_rows(self):
        self.gauss(self.find_max_element_and_put_it_in_step)

    def gauss(self, f=lambda: None):
        f()
        for step in range(self.n - 1):
            for row in range(step + 1, self.n):
                multiplier = self.elements[row][step] / self.elements[step][step]
                for column in range(step, self.n):
                    self.elements[row][column] = self.elements[row][column] - (multiplier * self.elements[step][column])

                self.result[row] = self.result[row] - (multiplier * self.result[step])

        self.inverse_transpose()

        for step in range(self.n - 1):
            for row in range(step + 1, self.n):
                multiplier = self.elements[row][step] / self.elements[step][step]
                for column in range(step, self.n):
                    self.elements[row][column] = self.elements[row][column] - (multiplier * self.elements[step][column])

                self.result[row] = self.result[row] - (multiplier * self.result[step])

        self.inverse_transpose()
                    # self.substitution()

    #    def check_if_system_of_equations_is_contraditory(self):
    #        for row in self.element:
    #            number_of_zeroes_in_row = 0
    #            for element in row:
    #                if element == 0:
    #                    number_of_zeroes_in_row ++
    #            if number_of_zeroes_in_row = self.n:
    #                return True
    #        return False

    # def substitution(self):
    #     solution = [0 for zeroes in range(self.n)]
    #     for row in range(self.n - 1, -1, -1):
    #         for column in range(row + 1, self.n):
    #             self.result[row] = self.result[row] - self.elements[row][column]
    #
    #         solution[row] = self.result[row] / self.elements[row][row]
    #
    #     print(solution)
    #     # def swap_solution(self,swapped_columns)

    def substitution(self):
        solution = [0 for zeroes in range(self.n)]
        for i in range(self.n):
            for j in range(self.n):
                self.elements[i][j] /= self.elements[i][i]

            self.result[i] /= self.elements[i][i]

        for i, solution in enumerate(self.result):
            print('x{} = {}'.format(i, solution))

if __name__ == '__main__':
    a = Matrix(3)
    a.input_from_list(MATRIX)
    try:
        a.gauss()
    except ZeroDivisionError:
        print('układ jest sprzeczny lub ')

    # a.gauss_with_swaping_columns_and_rows()
    a.output()
    a.substitution()
