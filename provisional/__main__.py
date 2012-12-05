import sys
import errno

from . import main

if len(sys.argv) <= 1:
    sys.stderr.write('Your have to append the module of your '
                     'provisional class. ERR:22\n')
    sys.exit(errno.EINVAL)

main(sys.argv[1:])
