import unittest
from copy import deepcopy

from main import GaussLinearEquationSystem, GaussWithOrderingEquationSystem


class GaussLinearEquationSystemUnitTest(unittest.TestCase):
    MATRICES_ANSWERS = [
        (
            [
                [1, -3, 2, 3],
                [1, 1, -2, 1],
                [2, -1, 1, -1],
            ],
            [-3 / 4, -11 / 4, -9 / 4],
        ),
        (
            [
                [2, -1, 1, -1],
                [1, -3, 2, 3],
                [1, 1, -2, 1],
            ],
            [-3 / 4, -11 / 4, -9 / 4],
        ),
        (
            [
                [1, 2, 2, 5],
                [3, -2, 1, -6],
                [2, 1, -1, -1],
            ],
            [-1, 2, 1],
        ),
        (
            [
                [1, 1, -1, 9],
                [0, 1, 3, 3],
                [-1, 0, -2, 2],
            ],
            [2 / 3, 7, -4 / 3],
        ),
    ]
    INVALID_MATRICES = [
        [
            [1, -3, 2, 3],
            [1, -3, 2, 3],
            [2, -1, 1, -1],
        ],
        [
            [1, -3, 2, 3],
            [1, -3, 2, 4],
            [2, -1, 1, -1],
        ],
        [
            [1, -3, 2, 3],
            [1, -3, 2, 4],
            [0, 0, 0, 0],
        ],
    ]

    matrix_class = GaussLinearEquationSystem

    def matrix_has_following_solutions(self, matrix, solutions):
        system = self.matrix_class()

        system.input_from_list(matrix)
        system_ = deepcopy(system)

        system.solve_system()

        self.assertTrue(system_.check_solutions(system.get_ordered_solutions()))
        if solutions is not None:
            for a, b in zip(system.get_ordered_solutions(), solutions):
                self.assertAlmostEqual(a, b)

    def test_solve_system(self):
        for i, (matrix, solutions) in enumerate(self.MATRICES_ANSWERS):
            with self.subTest(i=i):
                self.matrix_has_following_solutions(matrix, solutions)

    def test_solve_system_raises_exception_on_invalid_data(self):
        for i, matrix in enumerate(self.INVALID_MATRICES):
            with self.subTest(i=i):
                system = GaussLinearEquationSystem()
                system.input_from_list(matrix)
                with self.assertRaises(ZeroDivisionError):
                    system.solve_system()


class GaussWithOrderingLinearEquationSystemUnitTest(GaussLinearEquationSystemUnitTest):
    matrix_class = GaussWithOrderingEquationSystem


if __name__ == '__main__':
    unittest.main()
