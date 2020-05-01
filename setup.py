#!/usr/bin/python3
#import distutils.cmd
import os
#from distutils.command.clean import clean as _clean
#from distutils.command.clean import log
#from distutils.dir_util import remove_tree

from setuptools import setup
from setuptools.command.test import test

def readme(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

class BindTest(test):
    def finalize_options(self):
        super().finalize_options()
        self.test_suite = True
        self.test_args = []

    def run_tests(self):
        if not os.environ.get('TEST_NO_EXAMPLES'):
            script_path = os.path.dirname(os.path.realpath(__file__))


setup(
    name='ptrrecordsync',
    version='0.2.0',
    author='Dennis Cole III',
    author_email='dennis@lbsys.xyz',
    description='Creates PTR records for a DNS Zone',
    license='GPLv3',
    long_description=readme('README'),
    url='https://github.com/lightbulb703/ptrrecordsync',
    packages=['ptrrecordsync'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Internet :: Name Service (DNS)'
    ],
    entry_points={
        'console_scripts': ['ptrrecordsync = ptrrecordsync.__main__:main', ],
    }
)
