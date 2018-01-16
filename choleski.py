from copy import deepcopy
from math import sqrt

from gauss import GaussLinearEquationSystem


class CholeskiLinearEquationSystem(GaussLinearEquationSystem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._choleski_solutions = None

    def solve_system(self):
        # finding L and Lt
        L = GaussLinearEquationSystem(self.n)
        for s in range(L.n):
            for i in range(s, L.n):
                if s == i:
                    L._matrix[s][s] = sqrt(
                        self._matrix[s][s] - sum([
                            self._matrix[s][j] ** 2
                            for j in range(s - 2)
                        ])
                    )
                else:
                    L._matrix[i][s] = (
                        self._matrix[i][s] - sum([
                            (self._matrix[i][j] * self._matrix[s][j])
                            for j in range(s - 2)
                        ])
                    ) / L._matrix[s][s]

        Lt = deepcopy(L)
        Lt.transpose()

        L._free_members = self.get_ordered_solutions()
        L._reverse_act(to_upper_triangular=False)

        Lt._free_members = deepcopy(L.get_ordered_solutions())
        Lt._reverse_act()
        self._choleski_solutions = deepcopy(Lt.get_ordered_solutions())

    def print_results(self):
        if self._choleski_solutions is not None:
            self.print_math_results(self._choleski_solutions)
        else:
            raise ValueError('system nie jest do końca rozwiązany')

    def get_ordered_solutions(self):
        if self._choleski_solutions is not None:
            return self._choleski_solutions
        else:
            return self._free_members
