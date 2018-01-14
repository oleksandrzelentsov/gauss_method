from copy import deepcopy
from sys import exit

from decimal import Decimal, getcontext

PRECISION = 16


def input_safely(prompt: str = '', type_: type = str, validators=None):
    if validators is None:
        validators = []

    result = None
    while result is None:
        try:
            result = type_(input(prompt))
        except (ValueError, TypeError):
            continue

        for validator in validators:
            if not validator(result):
                result = None

    return result


class GaussLinearEquationSystem:
    EPSILON = Decimal("1e-{}".format(PRECISION - 2))

    def __init__(self, n=None):
        self._matrix = None
        self._free_members = None
        self._n = n

    @property
    def n(self):
        return self._n

    @n.setter
    def n(self, value: int):
        old_val = self.n
        try:
            self._n = value
            self._update_instance()
        except:
            self._n = old_val

    def get_ordered_solutions(self):
        return self._free_members

    @staticmethod
    def generate_matrix(n: int):
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
                elements[row].append(Decimal(0))

        return elements

    def input(self):
        self.n = input_safely('ilość zmiennych: ', int, validators=[
            lambda n: n > 1,
        ])
        for row in range(self.n):
            for column in range(self.n):
                self._matrix[row][column] = input_safely('A[{},{}]: '.format(row + 1, column + 1), Decimal)

            self._free_members[row] = input_safely('B[{}]: '.format(row + 1), Decimal)

    def input_from_list(self, matrix: list):  # used for testing
        self.n = len(matrix)
        for row in range(self.n):
            for column in range(self.n):
                self._matrix[row][column] = Decimal(matrix[row][column])

            self._free_members[row] = Decimal(matrix[row][self.n])

    def output(self, end_with: str = ''):
        for row in range(self.n):
            print('(', end='')
            for column in range(self.n):
                print('{0:10.2f}'.format(self._matrix[row][column]), end='')

            print(' |{0:10.2f}'.format(self._free_members[row]), end='')
            print(')')

        print(end_with.center(40, ' '))  # made to display an arrow in the middle of the screen

    def _make_zeroes_under(self, diagonal_index):
        for row in range(diagonal_index + 1, self.n):
            coefficient = self._matrix[row][diagonal_index] / self._matrix[diagonal_index][diagonal_index]
            for column in range(diagonal_index, self.n):
                self._matrix[row][column] -= (coefficient * self._matrix[diagonal_index][column])

            self._free_members[row] -= coefficient * self._free_members[diagonal_index]

    def _make_zeroes(self):
        """
        Make zeroes in matrix under each element on a diagonal line, using elementary matrix transformations.
        """
        for step in range(self.n - 1):
            self._make_zeroes_under(step)

    def _reverse_act(self):
        for row in list(range(self.n))[::-1]:
            diagonal_element = Decimal(self._matrix[row][row])

            left_part = Decimal(0)
            for column in range(row, self.n):
                if row != column:
                    left_part += self._matrix[row][column] * self._free_members[column]
                    self._matrix[row][column] = Decimal(0)
                else:
                    self._matrix[row][row] /= diagonal_element

            left_part /= diagonal_element
            self._free_members[row] /= diagonal_element
            self._free_members[row] -= left_part

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
        for i, solution in enumerate(self._free_members):
            numerator, denominator = solution.as_integer_ratio()
            if len(str(numerator)) > 4:
                pass
            else:
                if denominator != 1:
                    solution = '{} / {}'.format(numerator, denominator)
                else:
                    solution = int(solution)

            print('x{} = {}'.format(i + 1, solution))

        print()

    def check_solutions(self, solutions: list):
        """
        Check if a particular solution is correct.

        :param list solutions:
        """
        row_check_results = []
        for row, right_part in zip(self._matrix, self._free_members):
            left_part = Decimal(0)
            for element, solution in zip(row, solutions):
                left_part += element * solution

            row_check_results.append(abs(left_part - right_part) < self.EPSILON)

        if all(row_check_results):
            return True

        return False

    def _update_instance(self):
        self._matrix = self.generate_matrix(self.n)
        self._free_members = [Decimal(0)] * self.n

    def _transpose(self):
        new_one = self.generate_matrix(self.n)
        for row in range(self.n):
            for column in range(self.n):
                new_one[column][row] = self._matrix[row][column]

        self._matrix = new_one


class GaussWithOrderingEquationSystem(GaussLinearEquationSystem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._free_members_indices = None

    def _update_instance(self):
        super()._update_instance()
        self._free_members_indices = list(range(self.n))

    def _make_zeroes_under(self, diagonal_index):
        self._swap_rows_for_max_element_indices(diagonal_index)
        super()._make_zeroes_under(diagonal_index)

    def _maximum_element_indices(self, step: int):
        max_i = 0
        max_j = 0
        for row in range(self.n):
            if max(self._matrix[row][step:]) > self._matrix[max_i][max_j]:
                max_i, max_j = row, self._matrix[row].index(max(self._matrix[row][step:]))

        return max_i, max_j

    def _swap_rows_for_max_element_indices(self, step: int):
        max_i, max_j = self._maximum_element_indices(step)
        self.swap_columns(0, max_j)
        self.swap_rows(0, max_i)

    def swap_rows(self, row_1: int, row_2: int):
        self._matrix[row_1], self._matrix[row_2] = self._matrix[row_2], self._matrix[row_1]
        self._free_members[row_1], self._free_members[row_2] = self._free_members[row_2], self._free_members[row_1]

    def swap_columns(self, column_1: int, column_2: int):
        self._transpose()
        self._matrix[column_1], self._matrix[column_2] = self._matrix[column_2], self._matrix[column_1]
        self._free_members_indices[column_1], self._free_members_indices[column_2] = \
            self._free_members_indices[column_2], self._free_members_indices[column_1]
        self._transpose()

    def print_results(self):
        old_results = deepcopy(self._free_members)
        self._free_members = self.get_ordered_solutions()
        super().print_results()
        self._free_members = old_results

    def get_ordered_solutions(self):
        return [self._free_members[i] for i in self._free_members_indices]


def main(matrix_class):
    system = matrix_class()
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

    if system_.check_solutions(system.get_ordered_solutions()):
        print('poprawne ✓')
    else:
        print('niepoprawne ✗')


if __name__ == '__main__':
    getcontext().prec = PRECISION

    methods = [
        {
            'name': 'Zwykła metoda Gaussa',
            'class': GaussLinearEquationSystem
        },
        {
            'name': 'Metoda Gaussa z wyszukiwaniem elementu maksymalnego',
            'class': GaussWithOrderingEquationSystem,
        },
    ]
    for i, method in enumerate(methods):
        print('{i:2d}. {name}'.format(
            i=i + 1,
            **method,
        ))

    method_index = input_safely('wybierz metodę: ', int, validators=[
        lambda n: (1 <= n <= len(methods)),
    ])
    main(methods[method_index - 1]['class'])
