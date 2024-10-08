r"""Command-line tool to validate and pretty-print JSON

Usage::

    $ echo '{"json":"obj"}' | python -m json.tool
    {
        "json": "obj"
    }
    $ echo '{ 1.2:3.4}' | python -m json.tool
    Expecting property name enclosed in double quotes: line 1 column 3 (char 2)

"""
import sys
import json


def main():
    if len(sys.argv) == 1:
        infile = sys.stdin
        outfile = sys.stdout
    elif len(sys.argv) == 2:
        infile = open(sys.argv[1], "r")
        outfile = sys.stdout
    elif len(sys.argv) == 3:
        infile = open(sys.argv[1], "r")
        outfile = open(sys.argv[2], "w")
    else:
        raise SystemExit(sys.argv[0] + " [infile [outfile]]")
    with infile:
        try:
            obj = json.load(infile)
        except ValueError as e:
            raise SystemExit(e)
    with outfile:
        json.dump(obj, outfile, sort_keys=True, indent=4, separators=(",", ": "))
        outfile.write("\n")


if __name__ == "__main__":
    main()


__version__ = '0.1.0'
