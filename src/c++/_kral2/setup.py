#!/usr/bin/env python
# Copyright (c) 2020 Roman Trapeznikov
from distutils.core import setup, Extension

_kral2_module = Extension('_kral2', sources=['main.cc'])

setup(
    name='_kral2',
    version='1.0',
    description='kral2 internal module',
    ext_modules=[_kral2_module])
