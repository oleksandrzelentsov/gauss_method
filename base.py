from abc import abstractmethod, ABCMeta
from itertools import permutations

PRECISION = 6


class AbstractSystemOfEquations:
    __metaclass__ = ABCMeta
    EPSILON = 1e-4
    MAX_FRACTION_DIGITS = PRECISION

    def __init__(self, n=None):
        self._matrix = None
        self._free_members = None
        self._n = n
        self.n = n

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

    @abstractmethod
    def solve_system(self):
        pass

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
                elements[row].append(float(0))

        return elements

    def input(self):
        self.n = input_safely('ilość zmiennych: ', int, validators=[
            lambda n: n > 1,
        ])
        for row in range(self.n):
            for column in range(self.n):
                self._matrix[row][column] = input_safely('A[{},{}]: '.format(row + 1, column + 1), float)

            self._free_members[row] = input_safely('B[{}]: '.format(row + 1), float)

    def input_from_list(self, matrix: list):  # used for testing
        self.n = len(matrix)
        for row in range(self.n):
            for column in range(self.n):
                self._matrix[row][column] = float(matrix[row][column])

            self._free_members[row] = float(matrix[row][self.n])

    def output(self, end_with: str = ''):
        for row in range(self.n):
            print('(', end='')
            for column in range(self.n):
                print('{0:10.2f}'.format(self._matrix[row][column]), end='')

            print(' |{0:10.2f}'.format(self._free_members[row]), end='')
            print(')')

        print(end_with.center(40, ' '))  # made to display an arrow in the middle of the screen

    @classmethod
    def print_math_results(cls, results, letter='x'):
        for solution_number, solution in enumerate(results):
            numerator, denominator = solution.as_integer_ratio()
            if len(str(numerator)) > cls.MAX_FRACTION_DIGITS or len(str(denominator)) > cls.MAX_FRACTION_DIGITS:
                print('{}{} ≈ {:.3f}'.format(letter, solution_number + 1, solution))
            else:
                if denominator != 1:
                    solution = '{} / {}'.format(numerator, denominator)
                else:
                    solution = int(solution)

                print('x{} = {}'.format(solution_number + 1, solution))

        print()

    def print_results(self):
        """
        Pretty-print the results. To be called when the system is actually solved.
        """
        self.print_math_results(self._free_members)

    def check_solutions(self, solutions_: list):
        """
        Check if a particular solution is correct.

        :param list solutions:
        """
        for solutions in permutations(solutions_):
            row_check_results = []
            for row, right_part in zip(self._matrix, self._free_members):
                left_part = float(0)
                for element, solution in zip(row, solutions):
                    left_part += element * solution

                row_check_results.append(abs(left_part - right_part) < self.EPSILON)

            if all(row_check_results):
                return True

        return False

    def _update_instance(self):
        self._matrix = self.generate_matrix(self._n)
        self._free_members = [float(0)] * self._n

    def transpose(self):
        new_one = self.generate_matrix(self.n)
        for row in range(self.n):
            for column in range(self.n):
                new_one[column][row] = self._matrix[row][column]

        self._matrix = new_one

    @classmethod
    def compare(cls, a, b):
        return abs(float(a) - float(b)) < cls.EPSILON


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
