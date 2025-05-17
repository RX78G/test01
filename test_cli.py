import json, subprocess, sys, os, unittest
from calc import _HISTORY
class TestCLI(unittest.TestCase):
    def setUp(self):
        if _HISTORY.exists(): _HISTORY.unlink()
    def test_cli_list(self):
        # add 1 2 を実行し履歴保存
        subprocess.run([sys.executable, "cli.py", "--add", "1", "2"], check=True)
        # --list で JSON が返るか確認
        out = subprocess.check_output([sys.executable, "cli.py", "--list"], text=True)
        data = json.loads(out)
        self.assertEqual(data[0]["result"], 3)
if __name__ == "__main__":
    unittest.main(verbosity=2)