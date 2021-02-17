#!/usr/bin/env python
from setuptools import setup, find_packages, Distribution
import codecs
import os.path

# Make sure versiontag exists before going any further
Distribution().fetch_build_eggs('versiontag>=1.2.0')

from versiontag import get_version, cache_git_tag  # NOQA


packages = find_packages('src')

install_requires = [
    'celery>=4.3',
    'django>=2.2',
    'django-oscar>=3.0',
]

extras_require = {
    'development': [
        'coverage>=4.4.2',
        'flake8>=3.5.0',
        'freezegun>=0.3.12',
        'psycopg2cffi>=2.7.7',
        'PyYAML>=3.12',
        'sorl-thumbnail>=11.04',
        'tox>=2.9.1',
        'unittest-xml-reporting>=3.0.4',
        'versiontag>=1.2.0',

        # Needed for Oscar's web test framework
        'django-webtest>=1.9,<1.10',
        'WebTest>=2.0,<2.1',
    ],
}


def fpath(name):
    return os.path.join(os.path.dirname(__file__), name)


def read(fname):
    return codecs.open(fpath(fname), encoding='utf-8').read()


cache_git_tag()

setup(
    name='django-oscar-reports',
    description="An extension on-top of django-oscar that improves the Oscar Dashboard's report generation system",
    version=get_version(pypi=True),
    long_description=open('README.rst').read(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
    author='Craig Weber',
    author_email='crgwbr@gmail.com',
    url='https://gitlab.com/thelabnyc/django-oscar/django-oscar-reports',
    license='ISC',
    package_dir={'': 'src'},
    packages=packages,
    include_package_data=True,
    install_requires=install_requires,
    extras_require=extras_require,
)
