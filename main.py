from copy import deepcopy
from decimal import DivisionByZero, InvalidOperation
from sys import exit

from base import input_safely
from gauss import GaussLinearEquationSystem, GaussWithOrderingEquationSystem


def main(matrix_class):
    system = matrix_class()
    system.input()
    system_ = deepcopy(system)
    system.output('↓')
    try:
        system.solve_system()
    except (InvalidOperation, DivisionByZero):  # will occur if the system is not solvable
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
