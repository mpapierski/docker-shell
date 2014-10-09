import sys
import os
import json
from pwd import getpwuid
from grp import getgrgid

from helpers import _read_chunks, handle_os_errors

commands = {}

@handle_os_errors
def write(filename):
    with open(filename, 'wb') as f:
        for chunk in _read_chunks(sys.stdin):
            f.write(chunk)
        return 0

commands['write'] = write

@handle_os_errors
def read(filename):
    with open(filename, 'rb') as f:
        for chunk in _read_chunks(f):
            sys.stdout.write(chunk)
        sys.stdout.flush()
        return 0

commands['read'] = read

@handle_os_errors
def list(directory):
    dirs = []
    for path in os.listdir(directory):
        full_path = os.path.join(directory, path)
        st = os.stat(full_path)
        entry = {
            'name': path,
            'size': int(st.st_size),
            'directory': os.path.isdir(full_path),
            'permissions': st.st_mode,
            'hardlinks': st.st_nlink,
            'modified': int(st.st_mtime),
            'owner': getpwuid(st.st_uid)[0],
            'group': getgrgid(st.st_gid)[0],
        }
        dirs.append(entry)
    json.dump(dirs, sys.stdout, indent=4)
    sys.stdout.flush()
    return 0

commands['list'] = list

def main():
    chroot_dir = os.getenv('CHROOT_DIR')
    if chroot_dir is not None:
        os.chroot(chroot_dir)
    try:
        _, cmd, arg = sys.argv
    except ValueError:
        sys.stderr.write('Usage {} [command] [argument]\n'.format(sys.argv[0]))
    else:
        exit_code = commands[cmd](arg)
        sys.exit(1)

if __name__ == '__main__':
    main()
