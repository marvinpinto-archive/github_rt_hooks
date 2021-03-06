from setuptools import setup, find_packages
from os import mkdir, path

execfile('github_rt_hooks/version.py')

setup(
    name='github-rt-hooks',
    version=__version__,
    description='',
    author='',
    author_email='',
    url='',
    install_requires=open('setup-req.txt').readlines(),
    packages=find_packages(exclude=['test*']),
    include_package_data=True,
)
