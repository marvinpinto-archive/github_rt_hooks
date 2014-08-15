from setuptools import setup, find_packages
from os import mkdir, path
from github_rt_hooks import __version__

setup(
    name='github-rt-hooks',
    version=__version__,
    description='',
    author='',
    author_email='',
    url='',
    install_requires=open('setup-req.txt').readlines(),
    packages=find_packages(exclude=['ez_setup', 'test*']),
    include_package_data=True,
)
