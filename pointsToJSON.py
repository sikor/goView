import sys
import json

import encoder
import point


if len(sys.argv) != 2:
    print('usage: ' + sys.argv[0] + " inputFile outputFile")
    print("""Input file format example (2 points)
    10.0 25
    78 0.0
    """)
else:
    open(sys.argv[2], 'w').write(
        json.dumps([point.Point(float(line.split()[0]), float(line.split()[1])) for line in open(sys.argv[1])],
                   sort_keys=True, indent=4, separators=(',', ': '), default=encoder.default))



