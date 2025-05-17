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
        # 0割を防ぐため例外を送出する
        if b == 0:
            raise ZeroDivisionError("division by zero")
        return a / b
