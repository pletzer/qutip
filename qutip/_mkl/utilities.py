import os
import sys
from qutip.utilities import _blas_info
import qutip.settings as qset
from ctypes import cdll


def _set_mkl():
    """
    Finds the MKL runtime library for the
    Anaconda and Intel Python distributions.

    """
    imkl_dir = os.environ.get('EBROOTIMKL', '')
    if imkl_dir:
        # module imkl has been loaded
        imkl_version = os.environ['EBVERSIONIMKL']
        library = 'libmkl_rt.so'
        so_file = os.path.join(imkl_dir, 'mkl', imkl_version, 'lib', 'intel64', library)
        try:
            qset.mkl_lib = cdll.LoadLibrary(so_file)
            qset.has_mkl = True
	    print(f'QuTip will use {so_file}')
            return
        except:
            print(f'Could not open {so_file}')

    if (
        _blas_info() != 'INTEL MKL'
        or sys.platform not in ['darwin', 'win32', 'linux', 'linux2']
    ):
        return
    python_dir = os.path.dirname(sys.executable)
    if sys.platform in ['darwin', 'linux2', 'linux']:
        python_dir = os.path.dirname(python_dir)
    library = {
        'darwin': 'libmkl_rt.dylib',
        'win32': 'mkl_rt.dll',
        'linux': 'libmkl_rt.so',
        'linux2': 'libmkl_rt.so',
    }[sys.platform]

    if sys.platform in ['darwin', 'linux2', 'linux']:
        locations = [
            'lib',
            os.path.join('ext', 'lib'),
        ]
    else:
        locations = [
            os.path.join('Library', 'bin'),
            os.path.join('ext', 'lib'),
        ]

    for location in locations:
        try:
            qset.mkl_lib = cdll.LoadLibrary(
                os.path.join(python_dir, location, library)
            )
            qset.has_mkl = True
            return
        except Exception:
            pass
