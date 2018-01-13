from copy import deepcopy
from itertools import permutations
from sys import exit


class LinearEquationSystem:

    EPSILON = 1e-6

    def __init__(self, n=None):
        self.elements = None
        self.result = None
        self._n = n

    @property
    def n(self):
        return self._n

    @n.setter
    def n(self, value):
        old_val = self.n
        try:
            self._n = value
            self.elements = self.generate_matrix(self.n)
            self.result = [0] * self.n
        except:
            self._n = old_val

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
        n = None
        while n is None:
            try:
                n = int(input('ilość zmiennych: '))
            except (ValueError, TypeError):
                continue

        self.n = n
        for row in range(self.n):
            for column in range(self.n):
                el = None
                while el is None:
                    try:
                        el = float(input('A[{},{}]: '.format(row + 1, column + 1)))
                    except (ValueError, TypeError):
                        continue

                self.elements[row][column] = el

            self.result[row] = float(input('B[{}]: '.format(row + 1)))

    def input_from_list(self, matrix):  # used for testing
        self.n = len(matrix)
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

        print(end_with.center(44, ' '))  # made to display an arrow in the middle of the screen

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

    def _reverse_act(self):
        for row in list(range(self.n))[::-1]:
            diagonal_element = self.elements[row][row]

            left_part = 0
            for column in range(row, self.n):
                if row != column:
                    left_part += self.elements[row][column] * self.result[column]
                    self.elements[row][column] = 0
                else:
                    self.elements[row][row] /= diagonal_element

            left_part /= diagonal_element
            self.result[row] /= diagonal_element
            self.result[row] -= left_part

    def solve_system(self):
        """
        Solve the system using Gauss's method.
        """
        # zeroes in lower part of matrix
        self._make_zeroes()

        # reverse actions of Gauss algorithm
        self._reverse_act()

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

                row_check_results.append(abs(left_part - right_part) < self.EPSILON)

            if all(row_check_results):
                return True

        return False


if __name__ == '__main__':
    system = LinearEquationSystem()
    system.input()
    system_ = deepcopy(system)
    system.output('↓')
    try:
        system.solve_system()
    except ZeroDivisionError:  # will occur if the system is not solvable
        print('układ jest sprzeczny')
        exit(1)

    system.output()
    system.print_results()

    print('sprawdzam czy to jest poprawne rozwiązanie: ', end='')

    if system_.check_solutions(system.result):
        print('poprawne ✓')
    else:
        print('niepoprawne ✗')
