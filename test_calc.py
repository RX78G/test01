"""Unit tests for calc.py using unittest."""

import unittest

from calc import add, mul


class TestCalc(unittest.TestCase):
    """Tests for the add and mul functions."""

    def test_add(self):
        """add should return the sum of two numbers."""
        self.assertEqual(add(2, 3), 5)

    def test_mul(self):
        """mul should return the product of two numbers."""
        self.assertEqual(mul(2, 4), 8)


if __name__ == "__main__":
    unittest.main()
