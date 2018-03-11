from distutils.core import setup
from Cython.Build import cythonize
from distutils.extension import Extension

import numpy

extensions = [ Extension("dtw", sources = ["dtw.pyx"], include_dirs=[ numpy.get_include()])]

setup(
  name = 'dtw cythonized',
  ext_modules = cythonize(extensions)
  # ext_modules = extensions
)
