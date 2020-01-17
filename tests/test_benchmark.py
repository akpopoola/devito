import pytest
from os import path, listdir
from conftest import skipif
from devito.exceptions import CompilationError
from devito import configuration
from subprocess import CalledProcessError, check_call


pytestmark = skipif(['yask', 'ops'])


@pytest.mark.parametrize('mode', ['bench'])
@pytest.mark.parametrize('problem', ['acoustic', 'tti', 'elastic', 'viscoelastic'])
def test_bench(mode, problem):
    """
    Test combinations of modes x problems and created .json filename.
    Testing for both OpenMP enabled or disabled.
    """
    if configuration['openmp']:
        nthreads = configuration['platform'].cores_physical
    else:
        nthreads = 1

    command_bench = ['python', 'benchmarks/user/benchmark.py', mode, '-P', problem,
                     '-d', '40', '40', '40', '--tn', '20', '-x', '1']
    try:
        check_call(command_bench)
    except CalledProcessError as e:
        raise CompilationError('Command "%s" return error status %d. '
                               'Unable to compile code.\n' %
                               (e.cmd, e.returncode))
    dir_name = 'results/'

    base_filename = problem
    filename_suffix = '.json'
    arch = '_arch[unknown]'
    shape = '_shape[40,40,40]'
    nbl = '_nbl[10]'
    tn = '_tn[20]'
    so = '_so[2]'
    to = '_to[2]'
    dse = '_dse[advanced]'
    dle = '_dle[advanced]'
    at = '_at[aggressive]'
    nt = path.join('_nt[' + str(nthreads) + ']')
    mpi = '_mpi[False]'
    np = '_np[1]'
    rank = '_rank[0]'

    listdir("results/")

    bench_file = path.join(dir_name + base_filename + arch + shape + nbl + tn + so + to
                           + dse + dle + at + nt + mpi + np + rank + filename_suffix)

    command_plot = ['python', 'benchmarks/user/benchmark.py', 'plot', '-P', problem,
                    '-d', '40', '40', '40', '--tn', '20', '--max-bw', '12.8',
                    '--flop-ceil', '80', 'linpack']
    try:
        check_call(command_plot)
    except CalledProcessError as e:
        raise CompilationError('Command "%s" return error status %d. '
                               'Unable to compile code.\n' %
                               (e.cmd, e.returncode))

    bkend = '_bkend[core]'

    plot_file = path.join(dir_name + base_filename + shape + so + to + arch + bkend + at)

    assert path.isfile(bench_file)
    assert path.isfile(plot_file)

