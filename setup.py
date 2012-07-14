import os
from setuptools import setup, find_packages

def read_file(filename):
    """Read a file into a string"""
    path = os.path.abspath(os.path.dirname(__file__))
    filepath = os.path.join(path, filename)
    try:
        return open(filepath).read()
    except IOError:
        return ''


def get_readme():
    """Return the README file contents. Supports text,rst, and markdown"""
    for name in ('README', 'README.txt', 'README.rst', 'README.md'):
        if os.path.exists(name):
            return read_file(name)
    return ''


def get_install_requirements():
    requirements = []
    with open('requirements.txt') as file:
        temp = file.readlines()
        temp = [i[:-1] for i in temp]

        for line in temp:
            if line is None or line == '' or line.startswith(('#', '-e', 'git+', 'hg+')):
                continue
            else:
                requirements.append(line)
        return requirements

# Use the docstring of the __init__ file to be the description
DESC = " ".join(__import__('tokenauth').__doc__.splitlines()).strip()

setup(
    name="django-simple-tokenauth",
    version=__import__('tokenauth').__version__.replace(' ', '-'),
    url='',
    author='Tyler Butler',
    author_email='tyler.butler@microsoft.com',
    description=DESC,
    long_description=get_readme(),
    install_requires=get_install_requirements(),
    test_require=('django-nose', 'django-whatever'),
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    classifiers=[
        'Framework :: Django',
        ],
    )
