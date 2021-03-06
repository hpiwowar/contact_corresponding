import sys
import os

def password(f):
    f.password = True
    return f

def slow(f):
    f.slow = True
    return f

def online(f):
    f.online = True
    return f

def notimplemented(f):
    f.notimplemented = True
    return f

def acceptance(f):
    f.acceptance = True
    return f

def get_this_dir():
    module = sys.modules[__name__]
    this_dir = os.path.dirname(os.path.abspath(module.__file__))
    return(this_dir)

def set_testing_pythonpath():
    # from http://igotgenes.blogspot.com/2008_12_01_archive.html
    import os
    import sys

    parent_path = os.path.join(os.path.dirname(sys.argv[0]), os.pardir)
    sys.path.insert(0, os.path.abspath(parent_path))

def setup_module():
    set_testing_pythonpath()

def teardown_module():
	pass
