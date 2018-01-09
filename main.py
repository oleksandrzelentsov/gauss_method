from sys import exit


MATRIX = [
    [1, -3, 2, 3],
    [1, 1, -2, 1],
    [2, -1, 1, -1],
]

INVALID_MATRIX_1 = [
    [1, -3, 2, 3],
    [1, -3, 2, 3],
    [2, -1, 1, -1],
]


INVALID_MATRIX_2 = [
    [1, -3, 2, 3],
    [1, -3, 2, 4],
    [2, -1, 1, -1],
]


class LinearEquationSystem:

    def __init__(self, n):
        self.n = n
        self.elements = self.generate_matrix(self.n)
        self.result = [0,] * self.n

    @staticmethod
    def generate_matrix(n):
        """
        Generate square matrix of given order.
        Elements will be zeroes.

        :param int n: order of new matrix
        :return: created matrix
        :rtype: list
        """
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

    def input_from_list(self, matrix):  # used for testing
        for row in range(self.n):
            for column in range(self.n):
                self.elements[row][column] = matrix[row][column]

            self.result[row] = matrix[row][self.n]

    def output(self, end_with=''):
        for row in range(self.n):
            for column in range(self.n):
                print('{}'.format(self.elements[row][column]), end='  ')

            print('| {}'.format(self.result[row]))

        print(end_with)

    def rotate(self):
        """
        Rotate matrix 180 degrees. Results' order will also be reversed.
        """
        tr_result = self.generate_matrix(self.n)
        for row, reversed_row in zip(range(self.n), range(self.n)[::-1]):
            for column, reversed_column in zip(range(self.n), range(self.n)[::-1]):
                tr_result[reversed_row][reversed_column] = self.elements[row][column]

        self.elements = tr_result
        self.result = self.result[::-1]

    def _make_zeroes(self):
        """
        Make zeroes in matrix under each element on a diagonal line, using elementary matrix transformations.
        """
        for step in range(self.n - 1):
            for row in range(step + 1, self.n):
                multiplier = self.elements[row][step] / self.elements[step][step]
                for column in range(step, self.n):
                    self.elements[row][column] = self.elements[row][column] - (multiplier * self.elements[step][column])

                self.result[row] = self.result[row] - (multiplier * self.result[step])

    def solve_system(self):
        """
        Solve the system using Gauss's method.
        """
        # zeroes in lower part of matrix
        self._make_zeroes()

        # zeroes in upper part of matrix
        self.rotate()
        self._make_zeroes()

        # return it back
        self.rotate()

        # divide each column by its diagonal element to solve the system eventually
        for row in range(self.n):
            for column in range(self.n):
                self.elements[row][column] /= self.elements[row][row]

            self.result[row] /= self.elements[row][row]

    def print_results(self):
        """
        Pretty-print the results. To be called when the system is actually solved.
        """
        for i, solution in enumerate(self.result):
            print('x{} = {}'.format(i + 1, solution))


if __name__ == '__main__':
    system = LinearEquationSystem(3)
    system.input_from_list(MATRIX)
    system.output('↓')
    try:
        system.solve_system()
    except ZeroDivisionError:  # will occur if the system is not solvable
        print('układ jest sprzeczny')
        exit(1)

    system.output()
    system.print_results()
