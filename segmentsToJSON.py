import sys
import json

import encoder
import segment
import point


def main():
    if len(sys.argv) != 2:
        print('usage: ' + sys.argv[0] + " inputFile outputFile")
        print("""Input file format example (2 line segments)
        10.43 25 0 5
        78.0 0 15.0 4
        """)
    else:
        open(sys.argv[2], 'w').write(json.dumps(load(sys.argv[1]),
                                                sort_keys=True, indent=4, separators=(',', ': '),
                                                default=encoder.default))


def load(file_name):
    return [segment.Segment(
        point.Point(float(line.split()[0]), float(line.split()[1])),
        point.Point(float(line.split()[2]), float(line.split()[3]))) for line in open(file_name)]


if __name__ == "__main__":
    main()

