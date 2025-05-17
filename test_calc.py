"""Unit tests for Calculator class in calc.py."""

import unittest

from calc import Calculator


def _make_test(method_name, a, b, expected):
    def test(self):
        calc = Calculator()
        result = getattr(calc, method_name)(a, b)
        self.assertEqual(result, expected)
    return test


class TestCalculator(unittest.TestCase):
    pass


# Normal operation test cases for each method
_cases = {
    "add": (1, 2, 3),
    "sub": (5, 3, 2),
    "mul": (2, 3, 6),
    "div": (8, 2, 4),
}

for _name, _params in _cases.items():
    test_func = _make_test(_name, *_params)
    setattr(TestCalculator, f"test_{_name}", test_func)

def test_div_zero(self):
    calc = Calculator()
    with self.assertRaises(ZeroDivisionError):
        calc.div(1, 0)


setattr(TestCalculator, "test_div_zero", test_div_zero)


if __name__ == "__main__":
    unittest.main()
