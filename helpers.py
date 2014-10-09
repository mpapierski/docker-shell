import functools
import json
import sys

def handle_os_errors(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except OSError as e:
            json.dump({
                'errno': e.errno,
                'strerror': e.strerror,
            }, sys.stderr)
            sys.stdout.flush()
            return 1
        except IOError as e:
            json.dump({
                'errno': e.errno,
                'strerror': e.strerror
            }, sys.stderr)
            sys.stdout.flush()
            return 1
    return wrapper

def _read_chunks(fileobj, chunksize=16384):
    """Read chunks from `fileobj`
    """
    while True:
        chunk = fileobj.read(chunksize)
        if not chunk:
            break
        yield chunk