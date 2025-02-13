# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyPmwPatched(PythonPackage):
    """Schrodinger's Fork of Python megawidgets with essential patches applied.
       Pmw is a toolkit for building high-level compound widgets, or
       megawidgets, constructed using other widgets as component parts."""
    homepage = "https://github.com/schrodinger/pmw-patched"
    git = "https://github.com/schrodinger/pmw-patched"

    version('02-10-2020', commit='8bedfc8747e7757c1048bc5e11899d1163717a43')
