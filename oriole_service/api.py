""" Oriole-API """

import yaml
import code
from subprocess import run as sr
from os import path, walk, pardir, getcwd
from nameko.standalone.rpc import ClusterRpcProxy

exe = lambda s: sr(s, shell=True)
mexe = lambda f, s: tuple(map(f, s))
cwd = lambda: getcwd()
get_config = lambda f: get_yml(get_file(f))
test_cmd = "py.test -v --html=report.html"


def Config(name="services.cfg"):
    """ Obsoleted """
    return get_config(name)


def get_yml(f):
    with open(f) as filename:
        return yaml.load(filename)


def get_file(f):
    loc = cwd()
    for _ in range(3):
        config = path.join(loc, f)
        if path.isfile(config):
            return config
        loc = path.join(loc, pardir)


def get_path(f, loc):
    for fpath, _, fs in walk(loc):
        if f in fs:
            return fpath


def run(service):
    fmt = "cd %s && nameko run %s --config %s"
    config = path.join(cwd(), "services.cfg")
    fpath = get_path("%s.py" % service, "services")
    if fpath:
        exe(fmt % (fpath, service, config))


def remote_test(f):
    usage = 'Usage: s.log_service.ping()'
    config = get_yml(f)
    with ClusterRpcProxy(config) as s:
        code.interact(usage, None, {"s": s})


def mtest(test):
    fmt = "cd %s && %s"
    fpath = get_path("test_%s.py" % test, "tests")
    if fpath:
        exe(fmt % (fpath, test_cmd))


def test(tests):
    if not tests:
        exe(test_cmd)
    else:
        mexe(mtest, tests)