import pprint
import unittest
from copy import deepcopy
from itertools import permutations

from choleski import CholeskiLinearEquationSystem
from gauss import GaussLinearEquationSystem, GaussWithOrderingEquationSystem


class GaussLinearEquationSystemUnitTest(unittest.TestCase):
    MATRIX_CLASS = GaussLinearEquationSystem

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
        (
            [
                [1, 1, 0, 1, 0, -3],
                [2, 0, -1, 0, -2, 1],
                [1, -1, -2, 1, -2, 1],
                [2, 0, 1, 0, 1, -1],
                [-3, -1, 1, 2, 2, 1],
            ],
            [-0.5555555555555554, -2.111111111111111, 2.3333333333333335, -0.33333333333333326, -2.2222222222222223,],
        ),
        (
            [
                [1, -2, 3, 1, 1],
                [-2, 5, -8, 1, -1],
                [3, -8, 17, -7, 3],
                [1, 1, -7, 18, -4],
            ],
            [25 / 2, 3.5, -1, -3 / 2],
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

    MATRICES_TRANSPOSE = [
        (
            [
                [1, 0, 2],
                [2, 1, 1],
                [3, 2, 0],
            ],
            [
                [1, 2, 3],
                [0, 1, 2],
                [2, 1, 0],
            ]
        ),
        (
            [
                [1, 0, 2, 4],
                [2, 1, 1, 5],
                [3, 2, 0, 6],
                [5, 6, 7, 7],
            ],
            [
                [1, 2, 3, 5],
                [0, 1, 2, 6],
                [2, 1, 0, 7],
                [4, 5, 6, 7],
            ]
        ),
    ]

    MAKE_ZEROES_UNDER_TESTS = [
        (
            [
                [1, 2, 4],
                [3, 4, -2],
            ],
            [
                [1, 2, 4],
                [0, -2, -14],
            ],
            0,
        ),
    ]

    @staticmethod
    def matrix_object_equal_to_list_of_lists(matrix_obj, matrix_list):
        return matrix_list == [
            matrix_obj._matrix[row] + [matrix_obj.get_ordered_solutions()[row]]
            for row in range(matrix_obj.n)
        ]

    def matrix_has_following_solutions(self, matrix, solutions):
        system = self.MATRIX_CLASS()

        system.input_from_list(matrix)
        system_ = deepcopy(system)

        system.solve_system()

        solutions_from_matrix = system.get_ordered_solutions()
        if solutions is not None:
            permutation_equality = []
            for perm in permutations(solutions_from_matrix):
                answers = [
                    system.compare(a, b)
                    for a, b in zip(perm, solutions)
                ]
                permutation_equality.append(all(answers))

            self.assertTrue(
                any(permutation_equality),
                'lists \n{}\n{}\nare not equal'.format(
                    str(solutions_from_matrix),
                    str(solutions)
                )
            )

        self.assertTrue(
            system_.check_solutions(solutions_from_matrix),
            'manual check should not fail'
        )

    def test_solve_system(self):
        for i, (matrix, solutions) in enumerate(self.MATRICES_ANSWERS):
            with self.subTest(i=i, dim='{0}x{0}'.format(len(matrix))):
                self.matrix_has_following_solutions(matrix, solutions)

    def test_solve_system_raises_exception_on_invalid_data(self):
        for i, matrix in enumerate(self.INVALID_MATRICES):
            with self.subTest(i=i, dim='{0}x{0}'.format(len(matrix))):
                system = GaussLinearEquationSystem()
                system.input_from_list(matrix)
                with self.assertRaises(ZeroDivisionError):
                    system.solve_system()

    def test_transpose(self):
        for i, (matrix_arg, matrix_res) in enumerate(self.MATRICES_TRANSPOSE):
            with self.subTest(i=i):
                matrix = self.MATRIX_CLASS()
                matrix.input_from_list([row + [0] for row in matrix_arg])
                matrix.transpose()
                self.assertEqual(
                    matrix._matrix,
                    matrix_res,
                    'matrices should be transposed correctly'
                )

    def test_make_zeroes_under(self):
        for i, (matrix_a, matrix_b, step) in enumerate(self.MAKE_ZEROES_UNDER_TESTS):
            with self.subTest(i=i):
                matrix = self.MATRIX_CLASS()
                matrix.input_from_list(matrix_a)
                matrix._make_zeroes_under(step)
                self.assertTrue(
                    self.matrix_object_equal_to_list_of_lists(matrix, matrix_b),
                    'after 1 gaussian step it should have zeroes, matrix a, b:\n{}\n\n{}'.format(
                        pprint.pformat([
                            matrix._matrix[row] + [matrix.get_ordered_solutions()[row]]
                            for row in range(matrix.n)
                        ]),
                        pprint.pformat(matrix_b),
                    )
                )


class GaussWithOrderingLinearEquationSystemUnitTest(GaussLinearEquationSystemUnitTest):
    MATRIX_CLASS = GaussWithOrderingEquationSystem

    MAKE_ZEROES_UNDER_TESTS = [
        (
            [
                [1, 2, 4],
                [3, 4, -2],
            ],
            [
                [4, 3, 5],
                [0, -1 / 2, -2],
            ],
            0,
        ),
    ]


class CholeskiLinearEquationSystemUnitTest(GaussLinearEquationSystemUnitTest):
    MATRIX_CLASS = CholeskiLinearEquationSystem

    MATRICES_ANSWERS = [
        (
            [
                [1, -2, 3, 1, 1],
                [-2, 5, -8, 1, -1],
                [3, -8, 17, -7, 3],
                [1, 1, -7, 18, -4],
            ],
            [25 / 2, 3.5, -1, -3 / 2],
        ),
    ]


if __name__ == '__main__':
    unittest.main()
