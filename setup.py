#!/usr/bin/env python

import os

from setuptools import find_packages, setup

here = os.path.dirname(os.path.abspath(__file__))
f = open(os.path.join(here, 'README.md'))
long_description = f.read().strip()
f.close()


about = {}
with open('dj_rest_auth/__version__.py', 'r', encoding="utf8") as f:
    exec(f.read(), about)

setup(
    name='Agrisense Project',
    version=about['__version__'],
    author='Jeanos',
    author_email='jeankelouaouamouno71@gmail.com',
    url='https://github.com/Jeanos2004/Syllatah.git',
    description='Projet de Gestion Hebergement-Hotel',
    license='MIT',
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='django rest auth registration rest-framework django-registration api',
    zip_safe=False,
    install_requires=[
        'Django>=4.2,<6.0',
        'djangorestframework>=3.13.0',
    ],
    extras_require={
        'with-social': ['django-allauth[socialaccount]>=64.0.0'],
    },
    tests_require=[
        'coveralls>=1.11.1',
        'django-allauth>=64.0.0',
        'djangorestframework-simplejwt==5.3.1',
        'responses==0.12.1',
        'unittest-xml-reporting==3.2.0',
        'flake8==7.1.1',
    ],
    test_suite='runtests.runtests',
    include_package_data=True,
    python_requires='>=3.8',
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers FrontEnd',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ],
)
