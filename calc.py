import json
import pathlib
ROOT = pathlib.Path(__file__).resolve().parent
_HISTORY = ROOT / "history.json"
class Calculator:
    def add(self, a, b): return a + b
    def sub(self, a, b): return a - b
    def mul(self, a, b): return a * b
    def div(self, a, b):
        if b == 0:
            raise ValueError("ゼロでは割れません")
        return a / b
    def save(self, op, a, b, result):
        record = {"op": op, "a": a, "b": b, "result": result}
        history = []
        if _HISTORY.exists():
            history = json.loads(_HISTORY.read_text(encoding="utf-8"))
        history.append(record)
        _HISTORY.write_text(
            json.dumps(history, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
    def history(self):
        if _HISTORY.exists():
            return json.loads(_HISTORY.read_text(encoding="utf-8"))
        return []