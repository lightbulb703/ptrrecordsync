import os

from ptrrecordsync import __author__ as author
from ptrrecordsync import __version__ as version
from ptrrecordsync import __license__ as license
from ptrrecordsync import __maintainer__ as maintainer
from ptrrecordsync import __email__ as author_email
from ptrrecordsync import __url__ as url

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
    version=version,
    author=author,
    author_email=author_email,
    description='Creates PTR records for a DNS Zone',
    license=license,
    long_description=readme('README.md'),
    url=url,
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
