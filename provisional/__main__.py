import os
import sys
import errno

if len(sys.argv) <= 1:
    sys.stderr.write('Your have to append the module of your '
                     'provisional class. ERR:22\n')
    sys.exit(errno.EINVAL)

os.environ['PROVISIONAL_MODULE'] = sys.argv[1]

from . import app, load_config
try:
    load_config()

    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
except Exception as e:
    sys.stderr.write('Error while starting server: {} {}\n'.format(type(e), str(e)))
    sys.exit(errno.EINVAL)
