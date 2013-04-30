""" Some basic tools for command-line processing of Google Code Jam. """
import os
import sys
import subprocess

MY_MODULES = ['codejam_io', 'combinatorics', 'graphs', 'memo', 'primes']
CMD = ["C:\\Program Files\\7-Zip\\7z.exe", "u", "-tzip"]

class MultiOutput(object):
    """ A simple class to duplicate output into multiple output files.
    
    Makes an object that allows you to write to multiple files as though
    they were a single file (via the write() method, which is sufficient
    to also work for the print() function).

    You can also provide sys.stdout among those files, but it
    it will not be closed when the MultiOutput is closed.
    """
    def __init__(self, files):
        """ Creates the wrapper. """
        self._files = list(files)

    def close(self):
        """ Closes all wrapped files, except sys.stdout. """
        for f in self._files:
            if f != sys.stdout:
                f.close()

    def write(self, data):
        """ Writes the given data to all wrapped files. """
        for f in self._files:
            f.write(data)

def process_input(pfun, p0=lambda f:(int(f.readline()), None),
        module_path=None, argv=None):
    """ Processes a single Code Jam input file with some command-line tools.

    The arguments are two functions; - the first (pfun) takes
    four arguments - the input file, the output file, the current case 
    number, and any other case data (this is often None).

    The second only requires the input file, and should parse the file for
    the number of cases and any additional data that is needed; this
    data is passed onto pfun via its fourth argument.
    
    The command-line options are simple - a single input file is expected,
    defaulting to test.in if no file is given. By default, the output
    simply goes to stdout, but this is modified by two options:
        -d    Outputs to a file, which is named by replacing ".in" with ".out"
                on the end of the input filename, or by simply appending
                ".out" afterwards.
        -c    If -d was selected, the output will be copied to stdout as well
                as to the file.
    """
    if not argv:
        argv = sys.argv[1:]

    options = set()
    for arg in argv:
        if arg.startswith("-"):
            argv.remove(arg)
            options.update(arg[1:])
    filename = argv[0] if argv else 'test.in'

    targets = []
    if "d" in options:
        root, ext = os.path.splitext(filename)
        if ext == '.out':
            root += '.out'
        targets.append(open(root + '.out', 'w'))
    if not targets or "c" in options:
        targets.append(sys.stdout)
    if "n" in options:
        module_path = None
    f_out = MultiOutput(targets)

    with open(filename) as f_in:
        num_cases, other_data = p0(f_in)
        for case_no in range(1, num_cases+1):
            pfun(f_in, f_out, case_no, other_data)
    f_out.close()
    
    if module_path is not None:
        make_archive(module_path)

def make_archive(module_path):
    print()
    files = []
    target = os.path.join(os.path.split(module_path)[0], "src.zip")
    files.append(os.path.abspath(module_path))
    for module_name in sys.modules:
        if module_name in MY_MODULES:
            files.append(sys.modules[module_name].__file__)
    try:
        os.remove(target)
        print("Deleted {}".format(target))
    except OSError:
        pass
    command = CMD + [target] + files
    print("Running " + ' '.join(CMD))
    subprocess.call(CMD + [target] + files)
