import unittest
from calc import Calculator

class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()

    def test_add(self):
        self.assertEqual(self.calc.add(2, 3), 5)

    def test_sub(self):
        self.assertEqual(self.calc.sub(7, 4), 3)

    def test_mul(self):
        self.assertEqual(self.calc.mul(4, 6), 24)

    def test_div(self):
        self.assertEqual(self.calc.div(10, 2), 5.0)

    def test_div_zero(self):
        # ゼロ除算は ValueError が発生することを確認
        with self.assertRaises(ValueError):
            self.calc.div(1, 0)

if __name__ == "__main__":
    unittest.main(verbosity=2)
