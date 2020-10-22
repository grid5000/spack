# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class Libsigsegv(AutotoolsPackage, GNUMirrorPackage):
    """GNU libsigsegv is a library for handling page faults in user mode."""

    homepage = "https://www.gnu.org/software/libsigsegv/"
    gnu_mirror_path = "libsigsegv/libsigsegv-2.12.tar.gz"

    version('2.12', sha256='3ae1af359eebaa4ffc5896a1aee3568c052c99879316a1ab57f8fe1789c390b6')
    version('2.11', sha256='dd7c2eb2ef6c47189406d562c1dc0f96f2fc808036834d596075d58377e37a18')
    version('2.10', sha256='8460a4a3dd4954c3d96d7a4f5dd5bc4d9b76f5754196aa245287553b26d2199a')

    patch('patch.new_config_guess', when='@2.10')

    test_requires_compiler = True

    def configure_args(self):
        return ['--enable-shared']

    extra_install_tests = 'tests/.libs'

    @run_after('install')
    def setup_build_tests(self):
        """Copy the build test files after the package is installed to an
        install test subdirectory for use during `spack test run`."""
        self.cache_extra_test_sources(self.extra_install_tests)

    def test_link_and_run(self):
        """Check ability to link and run with libsigsegv."""
        data_dir = self.test_suite.current_test_data_dir
        prog = 'smoke_test'
        src = data_dir.join('{0}.c'.format(prog))

        compiler_options = [
            '-I{0}'.format(self.prefix.include),
            src,
            '-o',
            prog,
            '-L{0}'.format(self.prefix.lib),
            '-lsigsegv',
            '{0}{1}'.format(self.compiler.cc_rpath_arg, self.prefix.lib)]
        which('cc', required=True)(*compiler_options)

        # Now run the program and confirm the output matches expectations
        with open(data_dir.join('smoke_test.out'), 'r') as f:
            expected = f.read()
        output = which(prog)(output=str, error=str)
        assert expected in output

    def test_libsigsegv_unit_tests(self):
        """Run selected sigsegv tests from package unit tests"""
        passed = 'Test passed'
        checks = {
            'sigsegv1': [passed],
            'sigsegv2': [passed],
            'sigsegv3': ['caught', passed],
            'stackoverflow1': ['recursion', 'Stack overflow', passed],
            'stackoverflow2': ['recursion', 'overflow', 'violation', passed],
        }

        for cmd, expected in checks.items():
            exe = which(cmd)
            if not exe:
                # It could have been installed before we knew to capture this
                # file from the build system
                continue
            output = exe(output=str, error=str)
            for e in expected:
                assert e in output
