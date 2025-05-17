import argparse, json
from calc import Calculator, _HISTORY
def main() -> None:
    parser = argparse.ArgumentParser(description="Calculator CLI")
    parser.add_argument("--add", nargs=2, type=float, metavar=("A", "B"))
    parser.add_argument("--sub", nargs=2, type=float, metavar=("A", "B"))
    parser.add_argument("--mul", nargs=2, type=float, metavar=("A", "B"))
    parser.add_argument("--div", nargs=2, type=float, metavar=("A", "B"))
    parser.add_argument("--list", action="store_true", help="print history JSON")
    args = parser.parse_args()
    c = Calculator()
    if args.add:
        a, b = args.add; r = c.add(a, b); c.save("add", a, b, r); print(r)
    elif args.sub:
        a, b = args.sub; r = c.sub(a, b); c.save("sub", a, b, r); print(r)
    elif args.mul:
        a, b = args.mul; r = c.mul(a, b); c.save("mul", a, b, r); print(r)
    elif args.div:
        a, b = args.div; r = c.div(a, b); c.save("div", a, b, r); print(r)
    elif args.list:
        print(json.dumps(c.history(), ensure_ascii=False, indent=2))
    else:
        parser.print_help()
if __name__ == "__main__":
    main()