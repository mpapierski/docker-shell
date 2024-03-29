#!/usr/bin/env python
import sys
import os
import json
import stat
from pwd import getpwuid
from grp import getgrgid

from helpers import _read_chunks, _read_framed_chunks, handle_os_errors

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

def _json_stat(path):
    st = os.stat(path)
    try:
      owner = getpwuid(st.st_uid)[0]
    except KeyError:
      owner = 'root'
    try:
      group = getgrgid(st.st_gid)[0]
    except KeyError:
      group = 'root'
    return {
        'size': int(st.st_size),
        # Dont call os.path.isdir to avoid possible race condition
        'directory': st.st_mode & stat.S_IFDIR == stat.S_IFDIR,
        'permissions': st.st_mode,
        'hardlinks': st.st_nlink,
        'modified': int(st.st_mtime),
        'owner': owner,
        'group': group
    }

@handle_os_errors
def list(directory):
    dirs = []
    for path in os.listdir(directory):
        full_path = os.path.join(directory, path)
        st = _json_stat(full_path)
        dirs.append([path, st])
    json.dump(dirs, sys.stdout, indent=4)
    sys.stdout.flush()
    return 0

commands['list'] = list

@handle_os_errors
def stat_(path):
    st = _json_stat(path)
    json.dump(st, sys.stdout, indent=4)
    sys.stdout.flush()
    return 0

commands['stat'] = stat_

@handle_os_errors
def mkdir(arg):
    os.mkdir(arg)
    return 0

commands['mkdir'] = mkdir


@handle_os_errors
def rmdir(arg):
    os.rmdir(arg)
    return 0

commands['rmdir'] = rmdir

@handle_os_errors
def rm(arg):
    os.remove(arg)

commands['rm'] = rm

@handle_os_errors
def rename(src, dst):
    os.rename(src, dst)

commands['rename'] = rename


@handle_os_errors
def test_stdin(arg):
    import select
    import fcntl
    flags = fcntl.fcntl(sys.stdin, fcntl.F_GETFL)
    fcntl.fcntl(sys.stdin, fcntl.F_SETFL, flags | os.O_NONBLOCK)

    while True:
        r, w, e = select.select([sys.stdin], [], [], 1.0)
        if sys.stdin not in r:
            sys.stdout.write('Waiting...\n')
        else:
            data = sys.stdin.read()
            if not data:
                sys.stdout.write('EOF\n')
                sys.stdout.flush()
                break
            else:
                sys.stdout.write('Stdin "{!r}"\n'.format(data))
        sys.stdout.flush()

commands['test_stdin'] = test_stdin

def main():
    if len(sys.argv) < 3:
        sys.stderr.write('Usage {} [command] [argument]\n'.format(sys.argv[0]))
        return 1
    _ = sys.argv.pop(0)
    cmd = sys.argv.pop(0)
    return commands[cmd](*sys.argv)

if __name__ == '__main__':
    exit_code = main()
    if exit_code is None:
        exit_code = 0
    sys.exit(exit_code)
