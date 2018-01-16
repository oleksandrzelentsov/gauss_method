from copy import deepcopy

from base import AbstractSystemOfEquations


class GaussLinearEquationSystem(AbstractSystemOfEquations):
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

    def _reverse_act(self, to_upper_triangular=True):
        if to_upper_triangular:
            row_index_order = -1
        else:
            row_index_order = 1

        for row in list(range(self.n))[::row_index_order]:
            if to_upper_triangular:
                column_index_interval = (row, self.n)
            else:
                column_index_interval = (0, row + 1)

            diagonal_element = float(self._matrix[row][row])

            left_part = float(0)
            for column in range(*column_index_interval):
                if row != column:
                    left_part += self._matrix[row][column] * self._free_members[column]
                    self._matrix[row][column] = float(0)
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
        max_i, max_j = step, step
        for row in range(step, self.n):
            max_row = max(self._matrix[row][step:])
            if max_row > self._matrix[max_i][max_j] and max_row != float(0):
                max_i, max_j = row, self._matrix[row].index(max_row)

        return max_i, max_j

    def _swap_rows_for_max_element_indices(self, step: int):
        max_i, max_j = self._maximum_element_indices(step)
        self.swap_columns(step, max_j)
        self.swap_rows(step, max_i)

    def swap_rows(self, row_1: int, row_2: int):
        self._matrix[row_1], self._matrix[row_2] = self._matrix[row_2], self._matrix[row_1]
        self._free_members[row_1], self._free_members[row_2] = self._free_members[row_2], self._free_members[row_1]

    def swap_columns(self, column_1: int, column_2: int):
        self.transpose()
        self._matrix[column_1], self._matrix[column_2] = self._matrix[column_2], self._matrix[column_1]
        self._free_members_indices[column_1], self._free_members_indices[column_2] = \
            self._free_members_indices[column_2], self._free_members_indices[column_1]
        self.transpose()

    def _reset_solutions(self):
        self._free_members = self.get_ordered_solutions()
        self._free_members_indices = list(range(self.n))

    def print_results(self):
        old_results = deepcopy(self._free_members)
        self._free_members = self.get_ordered_solutions()
        super().print_results()
        self._free_members = old_results

    def _reverse_act(self, to_upper_triangular=True):
        super()._reverse_act(to_upper_triangular)
        # self._reset_solutions()

    def get_ordered_solutions(self):
        return [self._free_members[i] for i in self._free_members_indices]
