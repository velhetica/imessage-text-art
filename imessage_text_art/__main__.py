"""CLI: python -m imessage_text_art center < art.txt
     python -m imessage_text_art check < art.txt
"""
import sys
from .center import center_art, check_art

USAGE = "usage: python -m imessage_text_art [center|check] < art.txt"


def main(argv):
    if len(argv) != 2 or argv[1] not in ("center", "check"):
        print(USAGE, file=sys.stderr)
        return 2
    text = sys.stdin.read().rstrip("\n")
    if argv[1] == "check":
        warnings = check_art(text)
        if warnings:
            print("\n".join(warnings))
            return 1
        print("clean: every row centers, nothing wraps.")
        return 0
    try:
        print(center_art(text))
    except ValueError as e:
        print("error: %s" % e, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
