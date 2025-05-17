import unittest, json, pathlib
from calc import Calculator, _HISTORY
class TestHistory(unittest.TestCase):
    def setUp(self):
        if _HISTORY.exists():
            _HISTORY.unlink()
        self.c = Calculator()
    def test_save_and_load(self):
        r = self.c.add(2, 3)
        self.c.save("add", 2, 3, r)
        hist = self.c.history()
        self.assertEqual(hist[0]["result"], 5)
        self.assertTrue(_HISTORY.exists())
if __name__ == "__main__":
    unittest.main(verbosity=2)