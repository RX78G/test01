# calc.py
class Calculator:
    """四則演算をまとめたシンプルな電卓クラス"""

    def add(self, a: float, b: float) -> float:
        return a + b

    def sub(self, a: float, b: float) -> float:
        return a - b

    def mul(self, a: float, b: float) -> float:
        return a * b

    def div(self, a: float, b: float) -> float:
        # バグ: 0 割の例外処理を入れていない
        return a / b
