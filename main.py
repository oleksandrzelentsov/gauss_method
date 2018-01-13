from itertools import permutations
from sys import exit

from copy import deepcopy

EPSILON = 1e-5

MATRIX = [
    [1, -3,  2,  3],
    [1,  1, -2,  1],
    [2, -1,  1, -1],
]

INVALID_MATRIX_1 = [
    [1, -3,  2,  3],
    [1, -3,  2,  3],
    [2, -1,  1, -1],
]


INVALID_MATRIX_2 = [
    [1, -3,  2,  3],
    [1, -3,  2,  4],
    [2, -1,  1, -1],
]


class LinearEquationSystem:

    def __init__(self, n):
        self.n = n
        self.elements = self.generate_matrix(self.n)
        self.result = [0] * self.n

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
            print('(', end='')
            for column in range(self.n):
                print('{0:10.2f}'.format(self.elements[row][column]), end='')

            print(' |{0:10.2f}'.format(self.result[row]), end='')
            print(')')

        print(end_with)

    def rotate(self):  # TODO remove
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
                coefficient = self.elements[row][step] / self.elements[step][step]
                for column in range(step, self.n):
                    self.elements[row][column] -= (coefficient * self.elements[step][column])

                self.result[row] -= coefficient * self.result[step]

    def solve_system(self):
        """
        Solve the system using Gauss's method.
        """
        # zeroes in lower part of matrix
        self._make_zeroes()

        # divide each column by its diagonal element to solve the system eventually
        for row in range(self.n):
            coefficient = self.elements[row][row]
            for column in range(self.n):
                self.elements[row][column] /= coefficient

            self.result[row] /= coefficient

        # reverse actions of Gauss algorithm
        for row in list(range(self.n))[::-1]:
            left_part = sum([
                self.elements[row][column] * self.result[column]
                for column in range(row + 1, self.n)
            ])
            for column in range(row + 1, self.n):
                self.elements[row][column] = 0

            self.result[row] -= left_part

    def print_results(self):
        """
        Pretty-print the results. To be called when the system is actually solved.
        """
        for i, solution in enumerate(self.result):
            if not float(solution).is_integer():
                solution = '{} / {}'.format(*float(solution).as_integer_ratio())
            else:
                solution = int(solution)

            print('x{} = {}'.format(i + 1, solution))

        print()

    def check_solutions(self, unknowns):
        """
        Check if a particular solution is correct.

        :param list unknowns:
        """
        row_check_results = []
        for particular_solution_set in permutations(unknowns):
            row_check_results.clear()
            for row, right_part in zip(self.elements, self.result):
                left_part = 0
                for element, solution in zip(row, particular_solution_set):
                    left_part += element * solution

                row_check_results.append(abs(left_part - right_part) < EPSILON)

            if all(row_check_results):
                return True

        return False


if __name__ == '__main__':
    system = LinearEquationSystem(3)
    system.input_from_list(MATRIX)
    # system.input()
    system_ = deepcopy(system)
    system.output('↓')
    try:
        system.solve_system()
    except ZeroDivisionError:  # will occur if the system is not solvable
        print('układ jest sprzeczny')
        exit(1)

    system.output()
    system.print_results()

    print('sprawdzam czy to jest poprawne rozwiązanie....', end='')

    if system_.check_solutions(system.result):
        print('poprawnie ✓')
    else:
        print('NIEpoprawnie ✗')
