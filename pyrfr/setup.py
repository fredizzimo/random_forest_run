from distutils.command.build import build
from setuptools.command.install import install
from distutils.core import setup, Extension
import distutils.command.install as orig
from distutils.command.build_ext import build_ext


# Customize installation according to https://stackoverflow.com/a/21236111
class CustomBuild(build):
	def run(self):
		self.run_command('build_ext')
		build.run(self)


class CustomInstall(install):
	def run(self):
		self.run_command('build_ext')
		orig.install.run(self)


include_dirs = ['./include']

class BuildExt(build_ext):
	def build_extensions(self):
		extra_compile_args = []
		if self.compiler.compiler_type == 'msvc':
			extra_compile_args = ['/DNOMINMAX']
		else:
			extra_compile_args = ['-O2', '-std=c++11']
			#extra_compile_args = ['-g', '-std=c++11', '-O0', '-Wall']

		for e in self.extensions:
			e.extra_compile_args = extra_compile_args

		build_ext.build_extensions(self)


extensions = [	Extension(
					name = 'pyrfr._regression',
					sources=['pyrfr/regression.i'],
					include_dirs = include_dirs,
					swig_opts=['-c++', '-modern', '-features', 'nondynamic'] + ['-I{}'.format(s) for s in include_dirs],
				),
				Extension(
					name = 'pyrfr._util',
					sources=['pyrfr/util.i'],
					include_dirs = include_dirs,
					swig_opts=['-c++', '-modern', '-features', 'nondynamic'] + ['-I{}'.format(s) for s in include_dirs],
				)
			]

setup(
	name='pyrfr',
	version='${RFR_VERSION_MAJOR}.${RFR_VERSION_MINOR}.${RFR_VERSION_RELEASE}',
	author='Stefan Falkner',
	author_email='sfalkner@cs.uni-freiburg.de',
	license='Use as you wish. No guarantees whatsoever.',
	classifiers=['Development Status :: 3 - Alpha'],
	packages=['pyrfr'],
	ext_modules=extensions,
	python_requires='>=3',
	package_data={'pyrfr': ['docstrings.i']},
	py_modules=['pyrfr'],
	cmdclass={'build': CustomBuild, 'install': CustomInstall, 'build_ext': BuildExt},
)
