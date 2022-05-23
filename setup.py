'''Project Setup'''

import os
import sys
from setuptools import setup, find_packages
import versioneer
from setuptools.command.install import install

with open('README.md', 'r') as f:
    long_description = f.read()

with open('LICENSE') as f:
    license = f.read()


class VerifyVersionCommand(install):
    '''Verify GIT tag against the version

    Verify that the git tag matches our package version

    :param install: setuptools install
    '''

    description = 'verify that the git tag matches our package version'

    def run(self):
        version = versioneer.get_version()
        tag = os.getenv('CIRCLE_TAG')

        if tag != version:
            sys.exit(
                f'Failed version verification: "{tag}" does not match the version of this app: "{version}"'
            )


install_requires = ["wheel", "pydantic>=1.9.0", "loguru>=0.6.0", "pillow>=9.1.0", "versioneer"]

cmdclass = {
    "verify_version": VerifyVersionCommand,
}
cmdclass.update(versioneer.get_cmdclass())

setup(
    name='us-visa-appointment-notifier',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    author='Sai Varshith VV',
    author_email='svvarsham@gmail.com',
    url='https://github.com/amruthvvkp/us-visa-appointment-notifier',
    description=
    'This checks the appointments for US Visa against indian cities',
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires='>=3.7, !=3.9, != 3.10',
    packages=find_packages("src"),
    package_dir={"": "src"},   # tell distutils packages are under src
    install_requires=install_requires,
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries',
        'Intended Audience :: Developers'
    ],
    license='LGPLv3')