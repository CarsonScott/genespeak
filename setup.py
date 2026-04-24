from distutils.core import setup
import setuptools

setup(
	name='genespeak',
	version='1.0',
	description='A robust formal language for defining cellular-like dynamics.',
	author='Carson Scott',
	packages=setuptools.find_packages(),
	include_package_data=True,
	package_data={
	'genespeak': ['default/*.json']
	}
)